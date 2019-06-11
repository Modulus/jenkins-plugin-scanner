FROM python:alpine3.9

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt



ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]

EXPOSE 5000