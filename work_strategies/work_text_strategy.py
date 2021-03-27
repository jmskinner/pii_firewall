from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from work_strategies.work_base_strategy import WorkerBaseStrategy
from threading import Lock,Thread, Semaphore
from urllib.request import urlopen

class WorkerTextStrategy(WorkerBaseStrategy):

    def __init__(self,domain, task_type):
        super().__init__(domain, task_type)
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.text_generator = None
        self.thread_semaphore = Semaphore(2)
        self.my_lock = Lock()


    def _fetch(self, task):
        return task


    def _process(self, task):
        redacted_lines = {}
        results = []
        txt_lines_ordered = []
        local_threads = []

        if task.in_is_local:
            with open(task.in_endpoint) as fh:
                for pos, chunk in enumerate(self._read_in_chunks(fh)):
                        self.thread_semaphore.acquire()
                        thread = Thread(target=self._redact_a_chunk, args=(chunk,pos,redacted_lines,task.in_endpoint,results))
                        local_threads.append(thread)
                        thread.start()

        else:
            fh = urlopen(task.in_endpoint)
            for pos, chunk in enumerate(self._read_in_chunks(fh)):
                self.thread_semaphore.acquire()
                thread = Thread(target=self._redact_a_chunk, args=(chunk,pos,redacted_lines,task.in_endpoint,results))
                local_threads.append(thread)
                thread.start()



        for thread in local_threads:
            thread.join()

        for num, page in sorted(redacted_lines.items()):
            txt_lines_ordered.append(page)

        task.data = txt_lines_ordered
        task.profile['txt_NER'] = results
        return task


    def _push(self, worker, task):
        print(f"Worker {worker.id} pushed task at {task.in_endpoint}")
        worker.write_queue.put(task)

    def _redact_a_chunk(self,chunk,key,output,in_endpoint,results_list):
        self.my_lock.acquire()
        try:
            new_chunk = ''.join(str(e) for e in chunk)
            results = self.analyzer.analyze(text=new_chunk, language='en')
            results_list.extend(results)
            output[key] = self.anonymizer.anonymize(text=new_chunk,analyzer_results=results)
        except Exception:
            print(f"Incompatible text type occured on chunk {key+1} in the doc located at {in_endpoint}... ignoring this page")
        finally:
            self.my_lock.release()
            self.thread_semaphore.release()


    def _read_in_chunks(self,file_handler, block_size=1000):
        block = []
        for line in file_handler:
            block.append(line)
            if len(block) == block_size:
                yield block
                block = []

        if block:
            yield block
