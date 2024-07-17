# Use the official Python image as the base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 as base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the FastAPI app will be running on
EXPOSE 8000

# Start the FastAPI server
CMD [ "gunicorn", "-c", "gunicorn_conf.py", "-b", "0.0.0.0:8000", "src.main:app"]
