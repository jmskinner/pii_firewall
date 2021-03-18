from abc import ABC, abstractmethod


class WriterBaseStrategy(ABC):

    def __init__(self, domain, task_type):

        self.domain = domain
        self.task_type = task_type

    @abstractmethod
    def execute(self,writer,task):
        pass


class WriterNullStrategy(WriterBaseStrategy):

    def __init__(self):
        super().__init__(None,None)

    def execute(self,writer,task):
        print("I am a null type, you cannot execute me!")
