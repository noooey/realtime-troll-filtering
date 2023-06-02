# Dockerfile for FastAPI

# Use the official Python base image
FROM amd64/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY inference.py schema.py requirements.txt ./

# Install git
RUN apt-get update && apt-get install -y git

# Install the required packages
RUN pip install -U pip \
    && pip install -r requirements.txt
    # && pip install 'git+https://github.com/SKTBrain/KOBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'

# Expose the port for the FastAPI application
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]