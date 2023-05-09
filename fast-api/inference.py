from transformers import BertModel
from fastapi import FastAPI
import torch
import torch.nn as nn
import numpy as np
from kobert_tokenizer import KoBERTTokenizer
from schema import InputSchema, OutputSchema

tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')  
model = BertModel.from_pretrained("Haaaaeun/kobert_hatespeech")
max_seq_length=64

# Add a classification layer on top of the KoBERT model
classifier = nn.Sequential(
    nn.Linear(768, 1),
    nn.Sigmoid()
)

# Create FastAPI instance
app = FastAPI()

# Define the prediction endpoint
@app.post("/predict", response_model=OutputSchema)
def get_inference(input_data: InputSchema) -> OutputSchema:
    inputs = tokenizer(
        [input_data.sentence],
        max_length=max_seq_length,
        padding="max_length",
        truncation=True,
    )
    with torch.no_grad():
        sequence_output, pooled_output = model(**{k: torch.tensor(v) for k, v in inputs.items()})

        # Pass the pooled_output through the classifier to obtain the classification result
        classification_result = classifier(pooled_output)

        # Obtain the predicted class
        predicted_class = torch.round(classification_result).item()

        # Print the predicted class
        if predicted_class == 1:
            print("hate")
        else:
            print("not hate")

    print(OutputSchema(sentence=input_data.sentence, result=predicted_class))
    return OutputSchema(sentence=input_data.sentence, result=predicted_class)

# if __name__ == "__main__":
#     # Run FastAPI locally with uvicorn server
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)