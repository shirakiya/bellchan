from abc import ABCMeta, abstractmethod


class BaseMessageBuilder(metaclass=ABCMeta):

    @abstractmethod
    def create(self):
        pass
