from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, *args, **kwargs):
        pass

class Observable:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, event, *args, **kwargs):
        for observer in self._observers:
            observer.update(event, *args, **kwargs)
