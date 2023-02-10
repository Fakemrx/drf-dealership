FROM python:3.9

WORKDIR /Vasya/Docker/

COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system
#CMD ["pipenv", "install", "-r", "./requirements.txt"]

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]