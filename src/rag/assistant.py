from dataclasses import dataclass
from rag.vectorstoreservice import FaissService
from rag.documentservice import DocumentService
from rag.retrieverservice import BasicRetrieverService


DEFAULT_K= 5
@dataclass
class Assistant:
    """ Assistant Class"""
    pdf_path: str
    index_path: str
    k:int = DEFAULT_K

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
