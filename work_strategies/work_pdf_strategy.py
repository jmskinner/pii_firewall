from urllib.request import urlopen
from work_strategies.work_base_strategy import WorkerBaseStrategy
from pdf2image import convert_from_path, convert_from_bytes
from presidio_image_redactor import ImageRedactorEngine
from threading import Lock,Thread, Semaphore
from PIL import Image, ImageChops
from presidio_image_redactor.image_analyzer_engine import ImageAnalyzerEngine

class WorkerPDFStrategy(WorkerBaseStrategy):


    hyperthread_image_processing = True
    ## if we wanted to limit this across classes we could change this to active and remove it from the constructor
    # thread_semaphore = Semaphore(5)

    def __init__(self,domain, task_type):
        super().__init__(domain, task_type)
        self.my_lock = Lock()
        self.image_analyzer = ImageAnalyzerEngine()
        self.text_redactor = ImageRedactorEngine()
        self.thread_semaphore = None


    def _fetch(self, task):
        try:
            if task.in_is_local:
                task.data = convert_from_path(task.in_endpoint)
            else:
                data = urlopen(task.in_endpoint).read()
                task.data = convert_from_bytes(data, 'rb')
        except Exception:
            print(f'Error reading pdf from source: {task.in_endpoint}')

        return task


    def _process(self, task):
        redacted_images = {}
        local_threads = []
        pdf_img_list = []
        # self.thread_semaphore = Semaphore(task.config['max_thread_per_task']+1)
        # print(task.config['max_thread_per_task'])
        # In case we have a large doc, don't spin up too many threads
        for pos,image in enumerate(task.data):
            # self.thread_semaphore.acquire()
            thread = Thread(target=self._redact_an_image, args=(image,pos,redacted_images,task))
            local_threads.append(thread)

        for thread in local_threads:
            thread.start()
        # wait for the threads to finish
        for thread in local_threads:
            thread.join()

        # reassemble the doc in proper order
        for num, page in sorted(redacted_images.items()):
            pdf_img_list.append(page)


        task.data = pdf_img_list
        return task

    def _push(self, worker, task):
        print(f"Worker {worker.id} pushed task at {task.in_endpoint}")
        worker.write_queue.put(task)


    def _redact_an_image(self,img,key,output,task):
        self.my_lock.acquire()
        try:
            temp = ImageChops.duplicate(img)
            image_result = self.image_analyzer.analyze(temp)
            if len(image_result) > 0:
                task.profile["page"+str(key)] = str(image_result)
            output[key] = self.text_redactor.redact(img, self.REDACT_COLOR)
        except Exception:
            print(f"Incompatible PDF type occured on page {key+1} in the doc located at {task.in_endpoint}... ignoring this page")
            self.my_lock.release()
            # self.thread_semaphore.release()
        finally:
            self.my_lock.release()
            # self.thread_semaphore.release()


