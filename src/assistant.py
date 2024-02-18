from dataclasses import dataclass
from vectorstoreservice import FaissService
from documentservice import DocumentService
from retrieverservice import BasicRetrieverService

K= 5
@dataclass
class Assistant:
    """ Assistant Class"""
    pdf_path: str
    index_path: str
    k:int = K

    def __post_init__(self):
        """
        Initializes an instance of the class with the given parameters.
        """
        self.document_service = DocumentService(path=self.pdf_path)
        self.docs = self.document_service.get_docs()
        self.vector_store_service = FaissService(docs=self.docs, index_path=self.index_path)
        self.retriever_service =  BasicRetrieverService(self.vector_store_service, self.k)

    def request(self, question):
        return self.retriever_service.get_response(question)
