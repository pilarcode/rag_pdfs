from dataclasses import dataclass
from langchain_core.load import dumps, loads
#from langchain.retrievers import BM25Retriever
# from langchain.retrievers import SelfQueryRetriever
# from langchain.chains.query_constructor.base import AttributeInfo
# from langchain.retrievers import TfidfRetriever
# from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
# from langchain.retrievers import EnsembleRetriever
# from langchain.retrievers.multi_query import MultiQueryRetriever
# from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.prompts import ChatPromptTemplate
from vectorstoreservice import FaissService
from prompts import RAG_FUSION_PROMPT_TEMPLATE,PROMPT_TEMPLATE
from langchain_community.llms import Cohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.runnable import RunnableMap
from langchain_core.runnables import RunnableParallel

#from langchain.chains.combine_documents import create_stuff_documents_chain, create_summarization_chain
#from langchain.chains import create_retrieval_chain

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
    



# @dataclass
# class RagFusionRetrieverService:
#     """RagFusionRetrieverService Class"""
#     vector_store_service: FaissService
#     k: int

#     def __post_init__(self):
#         """Post initialization"""

#         self.prompt = ChatPromptTemplate.from_template(RAG_FUSION_PROMPT_TEMPLATE)
#         self.llm = Cohere(temperature=0)
#         self.output_parser = StrOutputParser()

        
#         self.index = self.vector_store_service.index
#         self.docs = self.vector_store_service.docs
#         self.retriever = self.index.as_retriever(search_kwargs={"k": self.k}, search_type="mmr")

#     def rank_fusion(self,results: list[list]):
#         fused_scores = {}
#         for docs in results:
#             for rank, doc in enumerate(docs):
#                 doc_str = dumps(doc)
#                 if doc_str not in fused_scores:
#                     fused_scores[doc_str] = 0
#                 fused_scores[doc_str] += 1 / (rank + self.k)

#         reranked_results = [(loads(doc), score) for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)]
#         return reranked_results


#     def get_relevant_documents(self, query):
    
#         generate_queries = (
#             self.prompt | self.llm |self.output_parser | (lambda x: x.split("\n"))
#         )

#         chain = generate_queries | self.retriever.map() | self.rank_fusion
#         docs_and_scores = chain.invoke({"query": query})
#         return docs_and_scores

    
#     def get_response(self, query:str):
#         """ Get response"""

#         items = self.get_relevant_documents(query)
#         context = [item for item in items]
#         print(context)

#         rag_chain = (
#             RunnableMap(
#                 {
#                     "context": lambda x: x["context"],
#                     "query": lambda x: x["query"],
#                 }
#             )
#             | self.prompt
#             | self.llm
#             | self.output_parser
#         )

#         response = rag_chain.invoke({"context": context,"query": query})
#         return response