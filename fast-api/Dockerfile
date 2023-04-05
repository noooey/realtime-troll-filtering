FROM amd64/python:3.9-slim

WORKDIR /usr/app

RUN pip install -U pip \
    && pip install "fastapi[all]"

COPY inference.py inference.py

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--reload"]