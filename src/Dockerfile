# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py ./
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for proxy configuration
ENV PROXY_HOST $PROXY_HOST
ENV PROXY_PORT $PROXY_PORT
ENV PROXY_USERNAME $PROXY_USERNAME
ENV PROXY_PASSWORD $PROXY_PASSWORD

# Set default values for host and port (can be overridden when running the container)
ENV HOST $HOST
ENV PORT $PORT

# Make port 5000 available to the world outside this container
EXPOSE $PORT

# Run the Python script with CMD
CMD ["python", "main.py"]
