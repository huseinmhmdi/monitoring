from abc import ABC, abstractmethod


class BaseService(ABC):

    @abstractmethod
    def request(self, data: dict):
        pass
