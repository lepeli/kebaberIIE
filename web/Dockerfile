FROM python:3.11-alpine

LABEL maintenair="Fatemeh Taherjouyan <fatemehtaherjouyan@gmail.com>"
LABEL description=""
LABEL nonroot="true"

# Setup the non root user

# Create a user and group

RUN addgroup -S appgroup && adduser -S app -G appgroup

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

USER app

COPY ./src/ /app

WORKDIR /app

# Install dependencies

RUN ["pip", "install", "-r", "requirements.txt"]

# Command baseline
CMD ["python", "-u", "index.py"]
