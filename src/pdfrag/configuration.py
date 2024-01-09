import os
from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv

@dataclass
class Configuration:
    def __init__(self):
        """
        Initializes an instance of the class.

        :param None: No parameters are required for this function.
        :return None: This function does not return any value.
        """
        # Load the environment variables from the .env file
        _ = load_dotenv(find_dotenv())

        # Set the environment variables for the index path and the vector store type
        self.vector_index_path = os.environ["VECTOR_INDEX_PATH"]
        self.vector_store_type = os.environ["VECTOR_STORE_TYPE"]

