FROM python:3.7.7-alpine3.11

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python","app.py"]