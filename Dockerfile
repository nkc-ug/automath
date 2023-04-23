FROM python:3 
ENV PYTHONUNBUFFERED 1 

WORKDIR /home

RUN apt-get update && \
    apt-get upgrade -y && \
    pip install django && \
    mkdir django

COPY ./django/ ./django

WORKDIR /home/django

RUN python3 manage.py migrate

CMD python3 manage.py runserver 0.0.0.0:8000