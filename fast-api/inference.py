from pydantic import BaseModel
# from transformers import KoBertModel
from transformers import BertModel
import torch
from fastapi import FastAPI, HTTPException

# Define InputSchema using Pydantic
class InputSchema(BaseModel):
    input_ids: list
    attention_mask: list

# Load the saved KoBERT model
model_path = 'saved_model.pt'
# model = KoBertModel.from_pretrained(model_path)
model = BertModel.from_pretrained("monologg/kobert")

# Create FastAPI instance
app = FastAPI()

# Define the prediction endpoint
@app.post("/predict")
async def predict(input_data: InputSchema):
    # Convert input data to torch tensors
    input_ids = torch.tensor(input_data.input_ids)
    attention_mask = torch.tensor(input_data.attention_mask)

    # Forward pass through the KoBERT model
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        inferred_value = outputs.pooler_output

    return {'inferred_value': inferred_value.tolist()}

if __name__ == "__main__":
    # Run FastAPI locally with uvicorn server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)