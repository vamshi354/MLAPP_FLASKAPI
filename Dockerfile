# Use full Python image (not slim)
FROM python:3.9



# Set the working directory
WORKDIR /app

# Install system dependencies required for spaCy and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    g++ \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model separately
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY . /app

# Expose the port
EXPOSE 5002

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:5002", "app:app"]
