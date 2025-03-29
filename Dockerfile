# Base image for Rasa Core
FROM rasa/rasa:3.5.0

# Set working directory
WORKDIR /app

# Install non-AVX TensorFlow version
RUN pip uninstall -y tensorflow && \
    pip install tensorflow-cpu==2.11.1 --no-cache-dir

# Copy your Rasa project files
COPY . /app

# Expose Rasa port
EXPOSE 5005

# Start the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]

