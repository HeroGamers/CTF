# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your script to the container
COPY main.py .

# Expose the port your server listens on
EXPOSE 777

# Run the casino script
CMD ["python", "main.py"]
