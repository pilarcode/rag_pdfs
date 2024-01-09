import os
from dataclasses import dataclass

from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
from langchain.vectorstores import DeepLake

from pdfrag.utils import logger

log = logger.get_logger(__name__)


@dataclass
class VectorIndex:
    docs: list
    index_path: str
    vector_db_type: str
    embedding_function: AzureOpenAIEmbeddings

    def __post_init__(self):
        """Post initialization"""
        if self.vector_db_type is None:
            raise ValueError(f"Invalid vector_db_type: {self.vector_db_type} at VectorIndex")

        if self.index_path is None:
            raise ValueError(f" Invalid index_path: {self.index_path} at VectorIndex")

        if not isinstance(self.embedding_function, AzureOpenAIEmbeddings):
            raise TypeError("embedding_function must be an instance of AzureOpenAIEmbeddings.")

        self.index = None
        self.index_2 = None

        if not os.path.exists(self.index_path):
            self.create_index()
        else:
            self.load_index()

    def create_index(self):
        """
        Creates the index and saves in self.index_path. The index is also saved in the attribute self.index.
        """

        log.debug(f"Create the index: {self.vector_db_type}  in this path {self.index_path}")
        if self.vector_db_type == "faiss":
            self.index = FAISS.from_documents(self.docs, self.embedding_function)
            self.index.save_local(self.index_path)

            log.debug(f"Docs in the vector store:{len(self.index.docstore._dict)}")

        elif self.vector_db_type == "chroma":
            self.index = Chroma.from_documents(
                documents=self.docs,
                embedding=self.embedding_function,
                persist_directory=self.index_path,
                collection_metadata={"hnsw:space": "cosine"},
            )
            log.debug(f"Docs in the vector store:{self.index._collection.count()}")

        else:
            self.index = DeepLake.from_documents(self.docs, dataset_path=self.index_path, embedding=self.embedding_function, overwrite=True)
            log.debug(f"Docs in the vector store:{len(self.index.vectorstore.dataset.id.numpy())}")

    def load_index(self):
        """
        Loads the index from self.index_path and saves it in self.index.
        """
        log.debug("Loading the existing index")

        if self.vector_db_type == "faiss":
            self.index = FAISS.load_local(self.index_path, self.embedding_function)
            log.debug(f"Docs loaded from the index {self.index_path}: {len(self.index.docstore._dict)}")

        elif self.vector_db_type == "chroma":
            self.index = Chroma(
                persist_directory=self.index_path,
                embedding_function=self.embedding_function,
                collection_metadata={"hnsw:space": "cosine"},
            )
            log.debug(f"Docs loaded from the index {self.index_path}: {self.index._collection.count()}")
        else:
            self.index = DeepLake(dataset_path=self.index_path, embedding=self.embedding_function,read_only = True)
            log.debug(f"Docs loaded from the index:{len(self.index.vectorstore.dataset.id.numpy())}")