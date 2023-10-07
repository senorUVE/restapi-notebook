FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install flask flask_sqlalchemy marshmallow requests

CMD ["python", "app.py"]
