from abc import ABC, abstractmethod
from write_strategies.write_base_strategy import WriterBaseStrategy

class WriterPDFStrategy(WriterBaseStrategy):

    def execute(self, writer, task):
        if len(task.data) > 1:
            task.data[0].save(task.out_endpoint, "PDF" ,resolution=100.0, save_all=True, append_images=task.data[1:])
        else:
            task.data[0].save(task.out_endpoint, "PDF" ,resolution=100.0, save_all=True)
