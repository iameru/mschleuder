FROM python:3.9

# Make a working directory
RUN mkdir /app
WORKDIR /app

# First, copy the requirements.txt only as it helps with caching
# Details: https://pythonspeed.com/articles/docker-caching-model/
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# Copy the source code
COPY . /app
COPY ./staging.env /app/.env

# Turn of debugging in production
ENV FLASK_DEBUG 0

# Set entrypoint
ENV FLASK_APP ms
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 80

# Run Flask command
CMD flask db upgrade ; gunicorn -w 4 -b 0.0.0.0:80 "ms:create_app()"
