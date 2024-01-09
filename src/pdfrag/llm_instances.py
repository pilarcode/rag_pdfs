import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from openai import AzureOpenAI

from pdfrag.utils import logger

log = logger.get_logger(__name__)
load_dotenv()



def get_embeddings_instance(
    azure_deployment=AZURE_EMBEDDINGS_DEPLOYMENT,
    openai_api_version=OPENAI_API_VERSION,
    chunk_size=CHUNK_SIZE,
):
    """
    Initialize and return an instance of the AzureOpenAIEmbeddings class for generating embeddings.

    Parameters:
        azure_deployment (str): The Azure deployment to use for the embeddings.
        openai_api_version (str): The OpenAI API version to use.
        chunk_size (int): The size of each chunk for splitting the input text.

    Returns:
        AzureOpenAIEmbeddings: An instance of the AzureOpenAIEmbeddings class.
    """

    embeddings_function = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_version=openai_api_version,
        chunk_size=chunk_size,
    )
    return embeddings_function


def get_llm_instance(
    azure_deployment=AZURE_LLM_DEPLOYMENT,
    openai_api_version=OPENAI_API_VERSION,
    temperature=0,
):
    """
    Initializes and returns an instance of the AzureChatOpenAI class.

    Parameters:
        azure_deployment (str): The Azure deployment to use for the AzureChatOpenAI instance. Defaults to AZURE_LLM_DEPLOYMENT.
        openai_api_version (str): The OpenAI API version to use for the AzureChatOpenAI instance. Defaults to OPENAI_API_VERSION.
        temperature (int): The temperature parameter to use for the AzureChatOpenAI instance. Defaults to 0.

    Returns:
        AzureChatOpenAI: An instance of the AzureChatOpenAI class.
    """

    llm_model = AzureChatOpenAI(
        azure_deployment=azure_deployment, openai_api_version=openai_api_version, temperature=temperature
    )
    return llm_model


client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)


def get_embedding(text, model=AZURE_EMBEDDINGS_DEPLOYMENT):
    """
    Gets the embedding for a given text using the specified model.

    Parameters:
        text (str): The input text to generate the embedding for.
        model (str, optional): The model to use for generating the embedding. Defaults to AZURE_EMBEDDINGS_DEPLOYMENT.

    Returns:
        str: The JSON representation of the embedding model dump.
    """
    response = client.embeddings.create(input=[text], model=model)
    return response.model_dump_json(indent=2)
