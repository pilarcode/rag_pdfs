from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Cohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.runnable import RunnableMap
from langchain_core.runnables import RunnableParallel
from rag.vectorstoreservice import FaissService
from prompts import PROMPT_TEMPLATE

@dataclass
class BasicRetrieverService:
    """RetrieverService Class"""
    vector_store_service: FaissService
    k: int

    def __post_init__(self):
        """Post initialization"""

        self.index = self.vector_store_service.index
        self.docs = self.vector_store_service.docs
        self.retriever = self.index.as_retriever(search_kwargs={"k": self.k}, search_type="mmr")
        self.llm = Cohere(temperature=0)
        self.prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.output_parser = StrOutputParser()
    
    
    def similarity_search_with_score(self, query):
        docs_and_scores = self.index.similarity_search_with_score(query, k=self.k)
        return docs_and_scores

    def get_relevant_documents(self, query):
        return self.retriever.get_relevant_documents(query)
    
    def get_response(self, query:str):
        """ Get response"""
        context = self.retriever.get_relevant_documents(query)

        rag_chain = (
            RunnableMap(
                {
                    "context": lambda x: x["context"],
                    "query": lambda x: x["query"],
                }
            )
            | self.prompt
            | self.llm
            | self.output_parser
        )

        response = rag_chain.invoke({"context": context,"query": query})
        return response
    
    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_response_with_source(self, query:str):
        """ Get response with sources"""
        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: self.format_docs(x["context"])))
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": self.retriever ,"query": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)
      
        response = rag_chain_with_source.invoke(query)
        return response
    
