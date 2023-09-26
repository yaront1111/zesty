# Stage 1: Build and install dependencies
FROM python:3.9-slim-bullseye AS build-stage

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code files into the build-stage container
COPY app/ ./app/

# Stage 2: Setup runtime
FROM python:3.9-slim-bullseye AS runtime-stage

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Copy Python dependencies
COPY --from=build-stage /usr/local /usr/local

# Copy the application code from the build-stage to the runtime-stage container
COPY --from=build-stage --chown=appuser:appuser /app /app

# Define working directory and switch to non-root user
WORKDIR /app

# Since your code resides inside 'app' folder in the container
WORKDIR /app/app

# Set Flask environment variables
ENV FLASK_APP=router.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 5000

CMD ["flask", "run"]
