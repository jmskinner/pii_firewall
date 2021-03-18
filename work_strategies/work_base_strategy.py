from abc import ABC, abstractmethod


class WorkerBaseStrategy(ABC):
    REDACT_COLOR = (0, 0, 0)
    def __init__(self, domain, task_type):

        self.domain = domain
        self.task_type = task_type

    def execute(self,worker,task):
        try:
            task = self._fetch(task)
            task = self._process(task)
            self._push(worker, task)
        except Exception:
            raise ValueError(f"Worker {worker.id} experienced an error processing {task.in_endpoint}...")

    @abstractmethod
    def _fetch(self, task):
        pass

    @abstractmethod
    def _process(self, task):
        pass

    @abstractmethod
    def _push(self, worker, task):
        pass

class WorkerNullStrategy(WorkerBaseStrategy):

    def __init__(self):
        super().__init__(None,None)

    def execute(self,writer,task):
        print("I am a null type, you cannot execute me!")

    def _fetch(self, task):
        print("I am a null type, you cannot fetch me!")


    def _process(self, task):
        print("I am a null type, you cannot process me!")

    def _push(self, worker, task):
        print("I am a null type, you cannot push me!")