# Use the latest Python image
FROM python:latest 

# Set the working directory of the container
WORKDIR /app 

# Copy over the requirements file
# This is order is best for caching
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy over the rest of the code
COPY . .

# Expose a port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]