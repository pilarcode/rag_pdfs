from dataclasses import dataclass

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers import BM25Retriever, ContextualCompressionRetriever, EnsembleRetriever, SelfQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from pdfrag.utils import logger

log = logger.get_logger(__name__)


@dataclass
class RetrieverQA:
    llm: object
    vector_index: object
    k: int

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.llm} at RetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.vector_index} at RetrieverQA")

        if self.k is None:
            self.k = 3

        self.retriever = self.vector_index.as_retriever(search_kwargs={"k": self.k})
        log.debug("RetrieverQA created")

    def get_relevant_documents(self, question):
        """
        Get relevant documents for a given question.

        Args:
            question (str): The question for which to retrieve relevant documents.

        Returns:
            list: A list of relevant documents.
        """
        return self.retriever.get_relevant_documents(question)
