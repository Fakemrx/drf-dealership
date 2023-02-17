FROM python:3.9

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./

RUN apt-get update
RUN apt install -y netcat

RUN pip install -U pipenv
RUN pipenv install --system

COPY . .

EXPOSE 8000

RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
