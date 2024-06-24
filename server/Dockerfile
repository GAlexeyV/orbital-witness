# server/Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock (if exists)
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
