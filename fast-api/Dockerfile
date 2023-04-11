# Dockerfile for FastAPI

# Use the official Python base image
FROM amd64/python:3.9-slim

# Copy the application files to the container
COPY inference.py requirements.txt /app/

# Set the working directory in the container
WORKDIR /app

# Install the required packages
RUN pip install -U pip \
    && pip install -r requirements.txt

# Download the KoBERT model files to the container
RUN mkdir ./models
COPY saved_model.pt /app/models/

# Expose the port for the FastAPI application
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]