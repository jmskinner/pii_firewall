import json
from write_strategies.write_base_strategy import WriterBaseStrategy

class WriterTextStrategy(WriterBaseStrategy):

    def _write_data(self, task):
        with open(task.out_endpoint, "w") as output:
             output.write(str(''.join(task.data)))

    def _write_profile(self, task):
        with open(task.profile_endpoint, "w") as outfile:
            json_profile = str(task.profile)
            outfile.write(json_profile)


