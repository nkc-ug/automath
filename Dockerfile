FROM python:3 
ENV PYTHONUNBUFFERED 1 
RUN pip install django && \
    mkdir /Autocal
