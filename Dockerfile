FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install OS dependencies for tricky packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN python -m pip install --upgrade pip setuptools wheel

# Install Python packages from requirements
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

# Copy app source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
