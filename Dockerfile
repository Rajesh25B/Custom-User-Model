#Image Inherited from python
FROM python:3.10.0a6-alpine3.13

LABEL author="Rajesh B"

# Set the Python unbuffered environment variable
# Recommended when running Python within Docker containers
# It doesn't allow Python to buffer the outputs. Just prints directly.
# This avoids complications with Docker image when running your Python app.
ENV PYTHONUNBUFFERED 1

# -- Store our dependencies in a requirements.txt file and copy to docker image
COPY ./requirements.txt /requirements.txt
# Encountered a WARNING after building. Need to add this line before postgresql
RUN apk update
# Add dependencies so we can install the psycopg2 package for Django/Postgres
RUN apk add --update --no-cache postgresql-client

RUN pip install -r /requirements.txt

# Create a 'app' file and make it the working DIR
RUN mkdir /app
# Make it as working directory
WORKDIR /app

# Copy the app file contents to our Docker image. 
COPY ./app /app

# Create a user that gonna run our app using Docker
RUN adduser -D user

# Finally switch to that user using USER
USER user