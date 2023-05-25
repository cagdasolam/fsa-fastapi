# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install the PostgreSQL development libraries and binaries
RUN apt-get update && apt-get install -y libpq-dev

# Copy the requirements.txt file
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file and prediction script
COPY . .

# Set the entry point to the prediction script
ENTRYPOINT ["python", "prediction.py"]

