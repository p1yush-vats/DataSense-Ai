# Use a stable Python version as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies, including git and git-lfs
RUN apt-get update && apt-get install -y git git-lfs

# Copy your requirements file first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "Home.py", "--server.port", "10000", "--server.headless", "true"]