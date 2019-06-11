FROM python:alpine3.9

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT "python" "main.py"