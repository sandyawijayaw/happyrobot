# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000 (matches gunicorn bind port)
EXPOSE 8000

# Command to run the app on port 8000
CMD ["gunicorn", "application:application", "--bind", "0.0.0.0:8000"]
