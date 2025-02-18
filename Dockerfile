FROM python:3.9.12-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "gunicorn",  "accounts_management.wsgi", "--preload", "--bind", "0.0.0.0:8000" ]