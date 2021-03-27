import mimetypes
import os
import threading
from local_threading.worker import Worker
from local_threading.writer import Writer
from multiprocessing import Queue
from tasking.task import Task
from pathlib import Path

class PIIFirewall:

    def __init__(self, config):
        self.runtime_config = config['runtime_config']
        self.task_config = config['task_config']
        self.task_queue = Queue()
        self.write_queue = Queue()
        self.worker_signals = Queue()
        self.writer_signals = Queue()
        self.max_num_workers = self.runtime_config['max_cpus']
        self.max_num_writers = self.runtime_config['max_threads']

    def run(self):

        reader_threads = []
        for endpoint in self.runtime_config['endpoints']:
            input_src, output_dest = endpoint.split("-->")
            input_src = input_src.strip()
            output_dest = output_dest.strip()
            if os.path.isdir(input_src):
                all_files = self.__get_all_files_endpoint(input_src)
                reader_thread = threading.Thread(target=self.__ingest_files, args=(all_files, output_dest))
                reader_threads.append(reader_thread)
            else:
                print("Not a directory, skipping for now")

        # spin up all the readers
        for reader_thread in reader_threads:
            reader_thread.start()

        # spin up all the workers
        worker_processes = []
        for worker_id in range(self.max_num_workers):
            # note that this is process not a queque
            worker = Worker(self.task_queue, self.write_queue, self.worker_signals, worker_id)
            worker_processes.append(worker)
            worker.start()

        # spin up writers
        writer_threads = []
        for writer_id in range(self.max_num_writers):
            # note that this is thread not a process
            writer = Writer(self.write_queue,self.writer_signals,writer_id)
            writer_threads.append(writer)
            writer.start()

        # wait for readers to be done
        for reader_thread in reader_threads:
            reader_thread.join()

        # let the workers know they can shutdown
        for worker in range(self.max_num_workers):
            self.task_queue.put(None)

        # wait while the workers finish
        for worker in worker_processes:
            worker.join()

        # once all the workers are done we let the writers know
        for writer in range(self.max_num_writers):
            self.write_queue.put(None)

        # we make main thread wait while the writers finish
        for writer in writer_threads:
            writer.join()


    def __get_mime_type(self, filename):
        return mimetypes.guess_type(filename)[0].split("/")


    def __get_all_files_endpoint(self, input_src):
        all_files = []
        for path, subdirs, files in os.walk(input_src):
            for name in files:
                if name[0] != ".":
                    all_files.append(os.path.join(path, name))
        return all_files


    def __ingest_files(self, all_files, dest):

        for in_endpoint in all_files:
            domain, file_type = self.__get_mime_type(in_endpoint)
            out_endpoint, profile_endpoint = self.__make_output_dest(domain, file_type, in_endpoint, dest)
            task = Task(domain, file_type, in_endpoint, out_endpoint,profile_endpoint,self.task_config)
            self.task_queue.put(task)
            print(f"Task at {task.in_endpoint} was placed on queue")


    def __make_output_dest(self, domain, file_type, file_name, dest):
        left_index = file_name.rfind("/")
        right_index = file_name.rfind(".")
        ext = file_name[right_index:]
        title = file_name[left_index+1:right_index]
        dir_path = os.path.join(dest,"data",domain,file_type)
        pro_path = os.path.join(dest,"profiles",domain,file_type)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        Path(pro_path).mkdir(parents=True, exist_ok=True)
        out_path = os.path.join(dir_path,title+"_post_pii_" + ext)
        profile_path = os.path.join(pro_path,title+".json")
        return out_path,profile_path
