from abc import ABC, abstractmethod




class DocumentEntry(ABC):

    @abstractmethod
    def as_document(self):
        pass