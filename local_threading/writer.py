from threading import Thread
from write_strategies.write_strategy_factory import WriterStrategyFactory
from write_strategies.write_base_strategy import WriterNullStrategy

class Writer(Thread):

    def __init__(self, write_queue, signal_queue, t_id):
        super(Writer, self).__init__()
        self.write_queue = write_queue
        self.signal_queue = signal_queue
        self.exec_strategy = WriterNullStrategy()
        self.id = t_id

    def __reassign_strategy(self, task):
        self.exec_strategy = WriterStrategyFactory.make_strategy(task)

    def run(self):

        for task in iter(self.write_queue.get, None):
            print(f"Writer {self.id} is working on {task.in_endpoint}..")
            if not WriterStrategyFactory.check_strategy(self.exec_strategy, task):
                self.__reassign_strategy(task)

            self.exec_strategy.execute(self, task)

        print(f"Writer {self.id} is shutting down now")
        self.signal_queue.put(1)




