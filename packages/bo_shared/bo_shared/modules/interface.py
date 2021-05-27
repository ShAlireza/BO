import abc


class BaseModule(abc.ABC):

    def __init__(self):
        pass

    def backup(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError
