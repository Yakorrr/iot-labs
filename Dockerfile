# Use the official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Run the main.py script inside the container when it starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

FROM python:latest
WORKDIR /usr/agent
ENV PYTHONPATH=/usr/agent
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
