from abc import ABC, abstractmethod


class BaseDataSource(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
