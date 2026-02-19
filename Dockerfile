FROM python:3.9-slim

# Install system dependencies for WeasyPrint and pdf2image
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for port (Cloud Run will override this)
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run the application with PORT environment variable
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT}
