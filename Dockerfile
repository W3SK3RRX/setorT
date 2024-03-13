FROM python:3

# Instalar as ferramentas do PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client-15 -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/