FROM python:alpine3.9

WORKDIR /opt/app

COPY . /opt/app
COPY requirements.txt /opt/app

RUN pip install -r requirements.txt



ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-t", "60", "main:app"]

EXPOSE 5000