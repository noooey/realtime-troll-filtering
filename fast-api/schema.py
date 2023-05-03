from pydantic import BaseModel

# Define InputSchema using Pydantic
class InputSchema(BaseModel):
    sentence: str

class OutputSchema(BaseModel):
    sentence: str
    result: str