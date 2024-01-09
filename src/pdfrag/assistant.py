from dataclasses import dataclass

from langchain.callbacks import get_openai_callback
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap
from langchain.output_parsers import PydanticOutputParser

from pdfrag.configuration import Configuration
from pdfrag.doc_loader import Loader
from pdfrag.llm_instances import get_embeddings_instance, get_llm_instance
from pdfrag.prompts import NOTE,LANGUAGE_PROMPT_TEMPLATE,ANSWER_PROMPT_TEMPLATE
from pdfrag.retriever import RetrieverQA
from pdfrag.utils import logger
from pdfrag.vector_store import VectorIndex
from pdfrag.data_models import Language

log = logger.get_logger(__name__)


@dataclass
class Assistant:
    docs_path: str
    specs_path: str
    vector_db_type: str
    vector_index_path: str

    def __post_init__(self):
        """
        Initializes an instance of the class with the given parameters.
        """

        self.config = Configuration()
        self.embedding_function = get_embeddings_instance()

        log.debug("- Loader")
        self.doc_loader = Loader(docs_path=self.docs_path, specs_path=self.specs_path)
        docs = self.doc_loader.extract_docs()

        log.debug("- Vector Index")
        self.vector_index = VectorIndex(
            docs,
            index_path=self.vector_index_path,
            vector_db_type=self.vector_db_type,
            embedding_function=self.embedding_function,
        )

        log.debug("- LLM")
        self.llm = get_llm_instance()

        log.debug("- Retriever")
        self.retriever = RetrieverQA(llm=self.llm, vector_index=self.vector_index.index, k=3)

    def detect_language(self, question):
        """
        Detects the language of a given question.

        Parameters:
            question (str): The question to detect the language of.

        Returns:
            Language: The detected language.

        """
        parser = PydanticOutputParser(pydantic_object=Language)

        detect_language_prompt = PromptTemplate(
            template=LANGUAGE_PROMPT_TEMPLATE,
            input_variables=["question"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )


        chain = LLMChain(llm=self.llm, prompt=detect_language_prompt)
        
        with get_openai_callback() as cb:
            response = chain.run(question)
            total_tokens = cb.total_tokens
            prompt_tokens = cb.prompt_tokens
            completion_tokens = cb.completion_tokens
            total_cost = cb.total_cost
       
        log.debug(f"prompt template: {LANGUAGE_PROMPT_TEMPLATE}")  
        log.debug(f"question: {question}")
        log.debug(f"response: {response}")
        log.debug(f"total tokens: {str(total_tokens)}")
        log.debug(f"prompt tokens: {str(prompt_tokens)}")
        log.debug(f"completion tokens: {str(completion_tokens)}")
        log.debug(f"completion total cost: {str(total_cost)}")

        language =  parser.parse(response)
        return language.value
    
    def request(self, question):
        """
        This function takes a question as input and returns the result of invoking a chain of operations.

        Parameters:
            question (str): The question to be passed to the chain of operations.

        Returns:
            The result of invoking the chain of operations with the given question.
        """

        language = self.detect_language(question)

        prompt = PromptTemplate(
            input_variables=["question","context","language"],
            template=ANSWER_PROMPT_TEMPLATE
        )

        context = self.retriever.get_relevant_documents(question)
        chain = (
            RunnableMap(
                {
                    "context": lambda x: x["context"],
                    "question": lambda x: x["question"],
                    "language": lambda x: x["language"],
                }
            )
            | prompt
            | self.llm
            | StrOutputParser()
        )

        with get_openai_callback() as cb:
            response = chain.invoke({"question": question, "context": context, "language": language}) + NOTE
            total_tokens = cb.total_tokens
            prompt_tokens = cb.prompt_tokens
            completion_tokens = cb.completion_tokens
            total_cost = cb.total_cost
     
        log.debug(f"prompt template: {ANSWER_PROMPT_TEMPLATE}")
        log.debug(f"question: {question}")
        log.debug(f"response: {response}")
        log.debug(f"language: {language}")
        log.debug(f"context: {str(context)}")
        log.debug(f"total tokens: {str(total_tokens)}")
        log.debug(f"prompt tokens: {str(prompt_tokens)}")
        log.debug(f"completion tokens: {str(completion_tokens)}")
        log.debug(f"completion total cost: {str(total_cost)}")
        return response
