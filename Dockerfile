# ./Dockerfile
FROM python:3.10
WORKDIR /usr/src/app

## Install packages
RUN  pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8000

CMD python manage.py runserver o.o.o.o:8000