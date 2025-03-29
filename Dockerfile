# Use Python 3.10 slim base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose port 5005 for Rasa server
EXPOSE 5005

# Run the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
