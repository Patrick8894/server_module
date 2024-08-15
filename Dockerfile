FROM python:3.8-slim

WORKDIR /server

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install -U pip

RUN pip install -r /app/requirements.txt

COPY ./app /server/app

EXPOSE 1234

CMD ["uvicorn", "app.main:server", "--host", "0.0.0.0", "--port", "1234", "--reload"]