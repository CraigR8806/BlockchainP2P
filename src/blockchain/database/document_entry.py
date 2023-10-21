from abc import ABCMeta, abstractmethod

class DocumentEntry(metaclass=ABCMeta):

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'as_document') and 
                callable(subclass.as_document) and 
                hasattr(subclass, 'from_document') and 
                callable(subclass.from_document))

    # @abstractmethod
    # def as_document(self):
    #     pass

