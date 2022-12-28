# ./Dockerfile
FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
RUN apt-get -y install libgl1-mesa-glx
RUN pip install -r requirements.txt
RUN pip install opencv-python

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]