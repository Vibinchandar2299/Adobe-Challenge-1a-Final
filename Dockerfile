# Use an official Python runtime as a parent image
# Changed from '3.9-slim-buster' to '3.9-slim-bullseye'
# Bullseye (Debian 11) is still actively supported.
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by PyMuPDF
# 'build-essential' for compiling, 'pkg-config' for finding libraries
# 'libssl-dev', 'libffi-dev', 'libjpeg-dev', 'zlib1g-dev' for PyMuPDF and other common Python libs
# 'poppler-utils' is often useful for PDF manipulation (though PyMuPDF handles many things itself)
# and can sometimes help with text extraction robustness in certain PDFs if PyMuPDF's default isn't enough.
# However, for core PyMuPDF function, it's not strictly necessary, but good to have if issues persist.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    # Optional: poppler-utils can provide tools like pdftotext, but not directly used by PyMuPDF itself
    # poppler-utils \
    # Clean up APT cache to keep the image size small
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the Python dependencies
# Use --no-cache-dir to avoid storing pip's cache, further reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container's /app directory
COPY . .

# Set the entrypoint for the container
ENTRYPOINT ["python", "main.py"]