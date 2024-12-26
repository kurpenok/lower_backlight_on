from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def send(self, *args):
        pass

    @abstractmethod
    def receive(self, *args, **kwargs):
        pass
