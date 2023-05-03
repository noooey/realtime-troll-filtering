from transformers import BertModel
from fastapi import FastAPI
import torch
import numpy as np
from kobert_tokenizer import KoBERTTokenizer
from schema import InputSchema, OutputSchema

tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')  
model = BertModel.from_pretrained("Haaaaeun/kobert_hatespeech")
max_seq_length=64

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
        print(sequence_output)
        test_eval=[]
        # for i in out:
        logits=sequence_output
        probs = logits.sigmoid()
        print('probs!!!!')
        print(probs)
        preds = (probs > 0.5).long()
        print('preds!!!!')
        print(preds)
        preds = preds.detach().cpu().numpy()
        print(preds.shape)

        if np.argmax(logits) >= 0.5:
            test_eval.append("부정적")
        else:
            test_eval.append("긍정적")
    print('**********')
    print(test_eval)
    print('**********')
    return OutputSchema(sentence=input_data.sentence, result=test_eval[0])
    # {
    #     "sentence": input_data.sentence,
    #     "result": test_eval[0],
    # }


if __name__ == "__main__":
    # Run FastAPI locally with uvicorn server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)