FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml .
COPY poetry.lock* .

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-root

# Copy application code
COPY . .

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]