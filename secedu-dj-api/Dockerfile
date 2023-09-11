FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /api

EXPOSE 9000

RUN pip install --upgrade pip

COPY ./requirements.txt /api/

RUN pip install -r requirements.txt

COPY ./ /api/

RUN chmod +x entrypoint.sh
