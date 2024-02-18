import os
from dataclasses import dataclass
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP=50

@dataclass
class DocumentService:
    """DocumentService Class"""
    path: str
    chunk_size: int = CHUNK_SIZE
    chunk_overlap: int = CHUNK_OVERLAP


    def __post_init__(self) -> None:
        """Initializes the object after it has been instantiated."""
    
        if not os.path.exists(self.path):
            raise ValueError(f"Invalid pdf path: {self.path}")   
             
        self.file_name = os.path.basename(self.path)
        self.extract_docs()

    def extract_docs(self):

        self.loader = PyPDFLoader(self.path)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size,
                                                       chunk_overlap=self.chunk_overlap)
        
        docs = self.loader.load_and_split(text_splitter=self.text_splitter)
        num_docs = len(docs)

        final_docs = []
        for i in range(num_docs):
            num_docs = docs[i].page_content
            page_content = docs[i].page_content
            page_label = docs[i].metadata['page']
            # Change the metadata labels
            metadata = {"pagina": page_label, "fichero": self.file_name}
            final_docs.append(Document(page_content=page_content, metadata=metadata))

        self.docs = final_docs

    def get_docs(self):
        """Returns the documents."""
        return self.docs