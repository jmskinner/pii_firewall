from write_strategies.write_base_strategy import WriterBaseStrategy
import json

class WriterImageStrategy(WriterBaseStrategy):

    def _write_data(self, task):
        task.data.save(task.out_endpoint)

    def _write_profile(self, task):
        with open(task.profile_endpoint, "w") as outfile:
            json.dump(task.profile, outfile)