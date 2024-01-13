FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /api
EXPOSE 7000

RUN apk update
RUN pip install --upgrade pip

#COPY ./entrypoint.sh /api/entrypoint.sh
#RUN chmod +x /api/entrypoint.sh

COPY ./requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt


COPY . /api

#ENTRYPOINT ["/bin/sh","/api/entrypoint.sh"]