# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for proxy configuration
ENV PROXY_HOST=127.0.0.1
ENV PROXY_PORT=40000
ENV PROXY_USERNAME=
ENV PROXY_PASSWORD=

# Set default values for host and port (can be overridden when running the container)
ENV HOST=0.0.0.0
ENV PORT=5000

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Python script with CMD
CMD ["python", "main.py"]
