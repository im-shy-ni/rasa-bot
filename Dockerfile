
# Stage 1: Rasa Dependencies
FROM python:3.10 AS rasa-stage
# Use Python 3.10 slim base image
FROM python:3.10-slim

# Set working directory

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir rasa==3.6.21 protobuf==4.23.3


# Stage 2: TensorFlow Dependencies
FROM python:3.10 AS tf-stage
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir tensorflow-cpu==2.11.1 protobuf==3.19.6

# Final Stage: Combine Both Environments
FROM python:3.10

# Copy the project files
COPY . .

# Expose port 5005 for Rasa server
EXPOSE 5005

COPY --from=rasa-stage /app /app
COPY --from=tf-stage /app /app

WORKDIR /app
CMD ["python", "run.py"]
