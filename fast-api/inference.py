from transformers import BertModel, AutoTokenizer
from fastapi import FastAPI
import torch
import torch.nn as nn
import requests
requests.get('https://www.huggingface.co')
from schema import InputSchema, OutputSchema

############# KoBERT #############
from kobert_tokenizer import KoBERTTokenizer
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
model = BertModel.from_pretrained("Haaaaeun/kobert_hatespeech")
####################################

########### SoonsilBERT ###########
# tokenizer = AutoTokenizer.from_pretrained("Haaaaeun/kcbert_hatespeech")
# model = BertModel.from_pretrained("Haaaaeun/kcbert_hatespeech")
####################################

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
    ############# KoBERT #############
    inputs = tokenizer(
        [input_data.sentence],
        max_length=max_seq_length,
        padding="max_length",
        truncation=True,
    )
    ####################################

    ########### SoonsilBERT ###########
    # inputs = tokenizer.encode_plus(
    #     input_data.sentence,
    #     add_special_tokens=True,
    #     return_attention_mask=True,
    #     return_tensors="pt"
    # )
    ####################################

    with torch.no_grad():
        ############# KoBERT #############
        sequence_output, pooled_output = model(**{k: torch.tensor(v) for k, v in inputs.items()})

        # Pass the pooled_output through the classifier to obtain the classification result
        classification_result = classifier(pooled_output)
        ####################################

        ########### SoonsilBERT ###########
        # outputs = model(
        #     inputs["input_ids"],
        #     attention_mask=inputs["attention_mask"]
        # )
        # # 출력층의 입력으로 사용하기 위해 reshape
        # outputs = outputs.pooler_output
        # classification_result = classifier(outputs)
        ####################################

        # Obtain the predicted class
        predicted_class = torch.round(classification_result).item()

        # Print the predicted class
        if predicted_class == 1:
            print("hate")
        else:
            print("not hate")

    print(OutputSchema(id=input_data.id, sentence=input_data.sentence, result=predicted_class))
    return OutputSchema(id=input_data.id, sentence=input_data.sentence, result=predicted_class)

# if __name__ == "__main__":
#     # Run FastAPI locally with uvicorn server
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
