# Use a base image that includes Python 3.12
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the working directory
COPY Pipfile Pipfile.lock /app/

# Install dependencies from the Pipfile.lock using pipenv
RUN pipenv install --system --deploy

# Copy the rest of your application code
COPY ./app /app

# Command to run the application
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
