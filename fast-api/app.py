from pydantic import BaseModel
# from transformers import KoBertModel
from transformers import BertModel
# import torch
from fastapi import FastAPI, HTTPException
# import tensorflow as tf

# Define InputSchema using Pydantic
class InputSchema(BaseModel):
    sentence: str
#     token_ids: list
#     valid_length: list
#     segment_ids: list
#     label: int

#     class Config:
#         arbitrary_types_allowed = True

# # Load the saved KoBERT model
# model_path = 'saved_model.pt'
# # model = KoBertModel.from_pretrained(model_path)
model = BertModel.from_pretrained("Haaaaeun/kcbert_hatespeech")
# print(fine_tuned_model_ckpt)

# from ratsnlp.nlpbook.ner import NERDeployArguments
# pretrained_model_name="beomi/kcbert-base"
# downstream_model_checkpoint_fpath='KoBERTmodel_state_dict.pt'
max_seq_length=64

# from transformers import BertTokenizer
# tokenizer = BertTokenizer.from_pretrained(
#     pretrained_model_name,
#     do_lower_case=False,
# )

from kobert_tokenizer import KoBERTTokenizer
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
"""
def inference_fn(sentence):
    inputs = tokenizer(
        [sentence],
        max_length=max_seq_length,
        padding="max_length",
        truncation=True,
    )
    with torch.no_grad():
        outputs = model(**{k: torch.tensor(v) for k, v in inputs.items()})
        print('***outputs***')
        print(outputs)
        probs = outputs.logits.sigmoid()
        print('***probs***')
        print(probs)
        # preds = (probs > 0.5).long()
        # preds = probs.argmax(dim=-1).squeeze() # apply argmax
        # print('zzz')
        # print(preds)
        # preds = (probs > 0.5).long().squeeze() # create preds using (probs > 0.5).long()
        # print('***preds***')
        # print(preds)
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        print('***tokens***')
        print(tokens)
        # print('***preds[0]***')
        # for pred in preds[0]:
        #     print(pred)
        # predicted_labels = [max(pred[1], pred[0]) for pred in preds[0]]
        predicted_labels = probs.argmax(dim=-1).squeeze()
        print('***predicted labels***')
        print(predicted_labels)
        result = []
        for token, predicted_label, prob in zip(tokens, predicted_labels, probs[0]):
            print(token, predicted_label, max(prob))
            if token not in [tokenizer.pad_token, tokenizer.cls_token, tokenizer.sep_token]:
                token_result = {
                    "token": token,
                    "predicted_label": predicted_label,
                    "prob": str(round(max(prob).item(), 4)),
                }
                result.append(token_result)
    return {
        "sentence": sentence,
        "result": result,
    }

import torch
fine_tuned_model_ckpt = torch.load(
    downstream_model_checkpoint_fpath,
    map_location=torch.device("cpu")
)

# print(fine_tuned_model_ckpt)

# from transformers import BertConfig
# pretrained_model_config = BertConfig.from_pretrained(
#     'skt/kobert-base-v1',
#     num_labels=fine_tuned_model_ckpt['classifier.bias'].shape.numel(), # num_labes == 2
# )

# from transformers import BertForTokenClassification
# import numpy as np
# model = BertForTokenClassification(pretrained_model_config)

# state_dic = {k: v for k, v in fine_tuned_model_ckpt.items() if k not in ["bert.pooler.dense.weight", "bert.pooler.dense.bias"]}

# model.load_state_dict(state_dic)

model.eval()
"""

# print(inference_fn('나는 정말 배가 고파 진짜로'))

# Create FastAPI instance
app = FastAPI()

# Define the prediction endpoint
@app.post("/predict")
def get_inference(input_data: InputSchema):
    # print(input_data.sentence)
    inference_fn(input_data.sentence)
    inputs = tokenizer(
        [input_data.sentence],
        max_length=max_seq_length,
        padding="max_length",
        truncation=True,
    )
    print(inputs)
    with torch.no_grad():
        out = model(**{k: torch.tensor(v) for k, v in inputs.items()})
        test_eval=[]
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()

            if np.argmax(logits) == 0:
                test_eval.append("부정적")
            else:
                test_eval.append("긍정적")
    return {
        "sentence": input_data.sentence,
        "result": test_eval[0],
    }
# async def predict(input_data: InputSchema):
#     # Convert input data to torch tensors
#     token_ids = torch.tensor(input_data.token_ids)
#     valid_length = input_data.valid_length
#     segment_ids = torch.tensor(input_data.segment_ids)

#     # Forward pass through the KoBERT model
#     with torch.no_grad():
#         outputs = model(input_ids=token_ids, valid_length=valid_length, segment_ids=segment_ids)
#         inferred_value = outputs.pooler_output

#     return {'inferred_value': inferred_value.tolist()}

if __name__ == "__main__":
    # Run FastAPI locally with uvicorn server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)