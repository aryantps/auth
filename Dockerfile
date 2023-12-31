# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for your application
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR $APP_HOME

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install

# Generate private_key.pem and public_key.pem
RUN openssl genpkey -algorithm RSA -out private_key.pem
RUN openssl rsa -pubout -in private_key.pem -out public_key.pem

# Copy the entire project directory into the container
COPY . .

# Install dbmate
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
RUN chmod +x /usr/local/bin/dbmate

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Apply database migrations using dbmate before running the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]