# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY app.py .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the command to run the Flask app when the container starts
CMD ["python", "app.py"]