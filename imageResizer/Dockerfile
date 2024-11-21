FROM python:3.11-alpine

LABEL maintenair="Yvan FOUCHER <contact@yvan.dev>"
LABEL description="Service used to compress images and convert them to png by default"
LABEL nonroot="true"

# Setup the non root user

# Create a user and group

RUN addgroup -S appgroup && adduser -S app -G appgroup

USER app

COPY ./src/ /app

WORKDIR /app

# Install dependencies

RUN ["pip", "install", "-r", "requirements.txt"]

# Command baseline
CMD ["python", "-u", "index.py"]
