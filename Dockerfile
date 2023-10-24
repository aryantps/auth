# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for your application
ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR $APP_HOME

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
