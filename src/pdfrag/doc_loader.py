import os
from dataclasses import dataclass
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

@dataclass
class Loader:
    """
    Docs Loader Class
    """
    pdf_path: str
    chunk_size: int = 3000
    chunk_overlap: int = 10


    def __post_init__(self) -> None:
        """
        Initializes the object after it has been instantiated.
        """
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,
                                                       chunk_overlap=self.chunk_overlap)

        if not os.path.exists(self.pdf_path):
            raise ValueError(f"Invalid pdf path: {self.pdf_path}")
        
        self.docs = self.extract_docs()
        

    def extract_docs(self):
        """
        Extract the pages/chunks from all the files in the docs_path
        """
        loader = PyMuPDFLoader(self.pdf_path)
        pages = loader.load()

        docs = [self.splitter.split_text(page.page_content) for page in pages]
        
        docs = [doc for doc in docs if doc]
        return docs

    def load(self):
        """
        Load the data from the instance variable `docs`.

        Returns:
            The data stored in the `docs` instance variable.
        """
    
        return self.docs