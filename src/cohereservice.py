import os
import cohere
from dataclasses import dataclass
from dotenv import load_dotenv,find_dotenv


import logging

logging.basicConfig(level=logging.DEBUG, filename='logs.log')
log = logging.getLogger(__name__)

@dataclass
class CohereService:
    """ Cohere Service"""
   
    def __post_init__(self):
        """Post initialization"""

        _= load_dotenv(find_dotenv(".env"))

        self.client = cohere.Client(os.environ["COHERE_API_KEY"])
        log.debug("Cohere client initialized")
        
       
    def embed_documents(self, texts:list, input_type="search_document"):
        response = self.client.embed(
                model=os.environ["COHERE_EMBEDDING_DEPLOYMENT"],
    			input_type=input_type,
                texts=texts)
         
        embeddings = response.embeddings
        return embeddings
    

    def embed_query(self, text:str, input_type="search_document"):
        response = self.client.embed(
                model=os.environ["COHERE_EMBEDDING_DEPLOYMENT"],
    			input_type=input_type,
                texts=[text])
         
        embeddings = response.embeddings
        return embeddings[0]

    def get_response(self,user_content:str):
        
        response = self.client.generate(
            prompt=user_content
        )
        return response.generations[0].text
    
