# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN pip install eventlet
# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make sure the database directory exists (PVC mount point)
RUN mkdir -p /active_database
VOLUME ["/active_database"]

# Expose the port the app runs on
EXPOSE 5201

# Run app.py when the container launches
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5201", "app:app"]