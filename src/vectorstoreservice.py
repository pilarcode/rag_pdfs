import os

from dataclasses import dataclass
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import DeepLake



@dataclass
class FaissService:
    docs: list
    index_path: str
    def __post_init__(self):
        """Post initialization"""
        if self.index_path is None:
            raise ValueError(f" Invalid index_path: {self.index_path} at VectorIndex")

        self.embeddings_function = CohereEmbeddings(model="embed-english-light-v3.0")
     
        if not os.path.exists(self.index_path):
            self.index = self.create_index()
        else:
            self.index =self.load_index()
        
        self.embeddings = self.get_embeddings()


    def create_index(self):
        self.index = FAISS.from_documents(self.docs, self.embeddings_function)
        self.index.save_local(self.index_path)
        #log("Docs in the vector store:", len(self.index.docstore._dict.items()))
        return self.index
    

    def load_index(self):
        print("Cargando el index")
        self.index=  FAISS.load_local(self.index_path, self.embeddings_function)
        return self.index

    def get_embeddings(self):
        texts = [docu.page_content for docu in self.docs]
        return self.index.embeddings.embed_documents(texts)
       

@dataclass
class ChromaService:
    docs: list
    index_path: str
    def __post_init__(self):
        """Post initialization"""
        if self.index_path is None:
            raise ValueError(f" Invalid index_path: {self.index_path} at VectorIndex")


        self.embeddings_function = CohereEmbeddings(model="embed-english-light-v3.0")
     
        if not os.path.exists(self.index_path):
            self.index= self.create_index()
        else:
            self.index= self.load_index()

        self.embeddings = self.get_embeddings()

    def create_index(self):
        self.index = Chroma.from_documents(
            documents=self.docs,
            embedding=self.embeddings_function,
            persist_directory=self.index_path,
            collection_metadata={"hnsw:space": "cosine"},
        )
        return self.index
    

    def load_index(self):
        self.index = Chroma(
            persist_directory=self.index_path,
            embedding_function=self.embeddings_function,
            collection_metadata={"hnsw:space": "cosine"},
        )
        #log.debug(f"Docs loaded from the index {self.index_path}: {self.index._collection.count()}")
        return self.index

    def get_embeddings(self):
        collection  = self.index._collection.get(include=['documents','embeddings'])
        return collection['embeddings']
    
          
@dataclass
class DeepLakeService:
    docs: list
    index_path: str

    def __post_init__(self):
        if self.index_path is None:
            raise ValueError(f" Invalid index_path: {self.index_path} at VectorIndex")

         
        self.embeddings_function = CohereEmbeddings(model="embed-english-light-v3.0")
   
        if not os.path.exists(self.index_path):
            self.index = self.create_index()
        else:
            self.index = self.load_index()

    def create_index(self):
        self.index = DeepLake.from_documents(self.docs, dataset_path=self.index_path, embedding=self.embeddings_function, overwrite=True)
        return self.index
    

    def load_index(self):
        self.index = DeepLake(dataset_path=self.index_path, embedding=self.embeddings_function,read_only = True)
        return self.index
    
    def get_embeddings(self):
        pass