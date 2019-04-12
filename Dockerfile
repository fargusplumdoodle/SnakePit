# Selecting image
FROM alpine:3.7

# This prevents python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1

# creating app directory
RUN mkdir /app
WORKDIR /app

# moving project files into app directory
COPY . .

# Installing requirements
RUN pip install -r requirements.txt

# Exposing port 8000 on tcp
EXPOSE 8000/tcp

# performing any database actions required
RUN python manage.py makemigrations
RUN python manage.py migrate

# defining run command, start server listening on port 8000 on all interfaces
CMD python manage.py runserver 0.0.0.0:8000
