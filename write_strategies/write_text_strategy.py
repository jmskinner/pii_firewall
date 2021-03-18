from abc import ABC, abstractmethod
from write_strategies.write_base_strategy import WriterBaseStrategy

class WriterTextStrategy(WriterBaseStrategy):

    def execute(self, writer, task):
        with open(task.out_endpoint, "w") as output:
             output.write(str(task.data[0]))