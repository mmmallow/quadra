from abc import ABC, abstractmethod

class EventListener(ABC):
    @abstractmethod
    def Listen(self, event, data):
        pass
