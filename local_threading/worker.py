from multiprocessing import Process
from work_strategies.work_strategy_factory import WorkerStrategyFactory
from work_strategies.work_base_strategy import WorkerNullStrategy

class Worker(Process):

    def __init__(self, task_queue,write_queue,signal_queue,w_id):
        super(Worker, self).__init__()
        self.task_queue = task_queue
        self.write_queue = write_queue
        self.signal_queue = signal_queue
        self.exec_strategy = WorkerNullStrategy()
        self.current_task = None
        self.id = w_id

    def __reassign_strategy(self, task):
        self.exec_strategy = WorkerStrategyFactory.make_strategy(task)


    def run(self):

        for task in iter(self.task_queue.get, None):
            print(f"Worker {self.id} is working on a {task.domain} task at  {task.in_endpoint}..")
            if not WorkerStrategyFactory.check_strategy(self.exec_strategy, task):
                self.__reassign_strategy(task)
            try:
                self.exec_strategy.execute(self, task)
            except Exception:
                pass

        print(f"Worker {self.id} is shutting down now")
        self.signal_queue.put(1)




