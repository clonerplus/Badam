# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables (optional)
ENV APP_NAME django
ENV PORT 8000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY python/django/django_requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r django_requirements.txt

# Copy the current directory contents into the container at /app
COPY ./python/django/manage.py /app/

COPY ./python/django/djangoProject/* /app/djangoProject/

# Expose the specified port for the Django application
EXPOSE ${PORT}

# Command to run your Django application (modify as needed)
CMD python manage.py runserver 0.0.0.0:${PORT}
