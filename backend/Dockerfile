# Use the Python version specified in your requirements/context
FROM python:3.12-slim 

# Set the working directory
WORKDIR /app

# Copy the requirements file and install all dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code (including your 'app/main.py', 'app/templates', 
# 'app/routers', and the 'Test' folder, as it is now inside the backend context).
COPY . .


# Expose the port for the web server
EXPOSE 8000

# Command to run the application using Uvicorn
# 'app.main:app' points to the 'app' variable inside 'main.py' within the 'app' module.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]