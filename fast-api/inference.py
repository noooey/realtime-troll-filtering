from fastapi import FastAPI
import torch
import torch.nn as nn
import requests
requests.get('https://www.huggingface.co')
from schema import InputSchema, OutputSchema

'''
model_name = ["Haaaaeun/kobert_hatespeech",
              "Haaaaeun/kcbert_hatespeech",
              "Haaaaeun/koELECTRA_hatespeech"]
'''

############# KoBERT #############
# from transformers import BertModel
# from kobert_tokenizer import KoBERTTokenizer
# tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
# model = BertModel.from_pretrained("Haaaaeun/kobert_hatespeech")
####################################

########### SoonsilBERT ###########
# from transformers import BertModel, AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("Haaaaeun/kcbert_hatespeech")
# model = BertModel.from_pretrained("Haaaaeun/kcbert_hatespeech")
####################################

########## KoELECTRA ###########
from transformers import AutoModelForSequenceClassification, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("Haaaaeun/koELECTRA_hatespeech")
model = AutoModelForSequenceClassification.from_pretrained("Haaaaeun/koELECTRA_hatespeech")
################################

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
    # inputs = tokenizer(
    #     [input_data.sentence],
    #     max_length=max_seq_length,
    #     padding="max_length",
    #     truncation=True,
    # )
    ####################################

    ########### SoonsilBERT ###########
    inputs = tokenizer.encode_plus(
        input_data.sentence,
        add_special_tokens=True,
        return_attention_mask=True,
        return_tensors="pt"
    )
    ####################################

    model.eval()
    with torch.no_grad():
        ############# KoBERT #############
        # sequence_output, pooled_output = model(**{k: torch.tensor(v) for k, v in inputs.items()})

        # # Pass the pooled_output through the classifier to obtain the classification result
        # classification_result = classifier(pooled_output)
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

        ############## KoELECTRA ##############
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        ##############################################################

        # Obtain the predicted class
        # predicted_class = torch.round(classification_result).item()

        # Print the predicted class
        if predicted_class == 1:
            print("hate")
            input_data.sentence = "*혐오적 표현으로 인해 제재된 댓글입니다.*"
        else:
            print("not hate")

    print(OutputSchema(id=input_data.id, sentence=input_data.sentence, result=predicted_class))
    return OutputSchema(id=input_data.id, sentence=input_data.sentence, result=predicted_class)

# if __name__ == "__main__":
#     # Run FastAPI locally with uvicorn server
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
