# Stage 1: Rasa Dependencies
FROM python:3.10 AS rasa-stage
WORKDIR /app                        # Set working directory
RUN mkdir -p /app                   # Ensure /app directory exists

COPY requirements.txt /app          
RUN pip install --no-cache-dir rasa==3.6.21 protobuf==4.23.3

# Stage 2: TensorFlow Dependencies
FROM python:3.10 AS tf-stage
WORKDIR /app                        # Set working directory
RUN mkdir -p /app                   # Ensure /app directory exists

COPY requirements.txt /app         
RUN pip install --no-cache-dir tensorflow-cpu==2.11.1 protobuf==3.19.6

# Final Stage: Combine Both Environments
FROM python:3.10
WORKDIR /app                        # Set the final working directory

# Copy files from previous stages
COPY --from=rasa-stage /app /app
COPY --from=tf-stage /app /app

# Copy the project files
COPY . .

# Expose port for Rasa
EXPOSE 5005

# Command to run the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
