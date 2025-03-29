# Use the official Rasa SDK image as the base
FROM rasa/rasa-sdk:3.5.0

# Switch to root user to have full permissions
USER root

# Upgrade pip with root privileges
RUN pip install --no-cache-dir --upgrade pip

# Install custom dependencies
RUN pip install --no-cache-dir requests beautifulsoup4

# Switch back to non-root user for security
USER 1000

# Copy the actions folder into the container
COPY . /app/actions

# Set the working directory
WORKDIR /app

# Start the action server
CMD ["start", "--actions", "actions"]

