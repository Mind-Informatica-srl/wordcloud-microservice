FROM python:3.14-rc-slim-bookworm

# Set the working directory
WORKDIR /app

# Install gcc, Poppler (for pdf2image), and basic fonts
RUN apt-get update && \
    apt-get install -y gcc poppler-utils ca-certificates && \
    apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Copy the fonts directory
COPY fonts /app/fonts

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "-u", "src/app.py"]