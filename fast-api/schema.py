from pydantic import BaseModel

# Define InputSchema using Pydantic
class InputSchema(BaseModel):
    id: str
    sentence: str

class OutputSchema(BaseModel):
    id: str
    sentence: str
    result: str
