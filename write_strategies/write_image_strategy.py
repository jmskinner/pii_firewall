from write_strategies.write_base_strategy import WriterBaseStrategy
from PIL import Image
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

class WriterImageStrategy(WriterBaseStrategy):

    def execute(self, writer, task):
        task.data.save(task.out_endpoint)
