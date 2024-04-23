FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8501

# Define the command to run your application
CMD ["streamlit", "run", "test.py"]
