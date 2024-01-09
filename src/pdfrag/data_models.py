from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

class Language(BaseModel):
    value: str = Field(description="The language of the text")
    