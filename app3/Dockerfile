FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY . .

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-root


# Run the application
CMD ["python", "main.py"]