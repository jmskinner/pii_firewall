from abc import ABC, abstractmethod


class WriterBaseStrategy(ABC):

    def __init__(self, domain, task_type):

        self.domain = domain
        self.task_type = task_type


    def execute(self,writer,task):
        self._write_data(task)
        self._write_profile(task)

    @abstractmethod
    def _write_data(self,task):
        pass

    @abstractmethod
    def _write_profile(self,task):
        pass


class WriterNullStrategy(WriterBaseStrategy):

    def __init__(self):
        super().__init__(None,None)

    def _write_data(self,task):
        print("I am a null type, you cannot execute me!")

    def _write_profile(self,task):
        print("I am a null type, you cannot execute me!")
