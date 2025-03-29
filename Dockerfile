# Use Python 3.10 base image
FROM python:3.10-slim

# Switch to root user to avoid permission issues
USER root

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install non-AVX TensorFlow version with root permissions
RUN pip uninstall -y tensorflow && \
    pip install tensorflow-cpu==2.11.1 --no-cache-dir

# Copy the project files
COPY . .

# Switch back to non-root user
USER 1001

# Run the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
