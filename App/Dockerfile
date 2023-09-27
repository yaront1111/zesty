# Stage 1: Build and install dependencies
FROM python:3.9-slim-bullseye AS build-stage

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Stage 2: Setup runtime
FROM python:3.9-slim-bullseye AS runtime-stage

RUN useradd -m appuser
USER appuser

COPY --from=build-stage /usr/local /usr/local
COPY --from=build-stage --chown=appuser:appuser /app/app /app

WORKDIR /app

ENV FLASK_APP=router.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 5000

CMD ["flask", "run"]
