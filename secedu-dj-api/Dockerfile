FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /api

EXPOSE 9000

RUN pip install --upgrade pip

COPY ./requirements.txt /api/

RUN pip install -r requirements.txt

COPY ./ /api/

CMD python manage.py migrate --noinput || exit 1 && \
    python manage.py collectstatic --noinput || exit 1 && 

CMD gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:9000 core.wsgi
