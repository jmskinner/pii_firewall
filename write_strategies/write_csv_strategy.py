from write_strategies.write_base_strategy import WriterBaseStrategy

class WriterCSVStrategy(WriterBaseStrategy):

    def execute(self, writer, task):
        task.data.to_csv(task.out_endpoint,index=False)