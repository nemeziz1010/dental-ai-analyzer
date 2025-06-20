# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# --- FIX: Install system dependencies required by OpenCV ---
# The python:3.11-slim image is minimal and lacks some libraries needed by cv2.
# We add both libgl1-mesa-glx and the new one, libglib2.0-0.
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the requirements file into the container
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container
COPY ./api /app/api
COPY ./core /app/core
COPY ./models /app/models
COPY ./services /app/services
COPY ./main.py /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
# Use --host 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
