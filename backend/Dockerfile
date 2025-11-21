# Code from https://www.digitalocean.com/community/tutorials/create-fastapi-app-using-docker-compose

FROM python:3.12-slim 

# Set the working directory
WORKDIR /app

# Copy the requirements file and install all dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code to the container
COPY . .

# Port for the web server
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]