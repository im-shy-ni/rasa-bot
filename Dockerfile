# Base stage: Install dependencies
FROM python:3.10 AS base
WORKDIR /app
RUN mkdir -p /app

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

# Final stage: Install Rasa and TensorFlow in the final image
FROM python:3.10
WORKDIR /app

# Copy installed dependencies from the base stage
COPY --from=base /app /app

# Install compatible versions of Rasa and TensorFlow
RUN pip install --no-cache-dir rasa==3.6.21 tensorflow-cpu==2.12.0

# Copy the project files
COPY . .

# ✅ Use Railway's dynamic port
EXPOSE $PORT

# Start Rasa server using the dynamic port
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug", "-p", "${PORT}"]
