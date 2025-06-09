FROM python:3.13.3-slim

# Set the working directory
WORKDIR /app

# Install gcc
RUN apt-get update && apt-get install -y gcc

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the fonts directory
COPY fonts /app/fonts

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "-u", "src/app.py"]