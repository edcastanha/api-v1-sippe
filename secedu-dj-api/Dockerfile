FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /api
EXPOSE 9000
RUN pip install --upgrade pip
COPY ./requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
COPY ./ /api/
COPY ./entrypoint.sh /api/entrypoint.sh

RUN chmod +x entrypoint.sh

CMD ["python", "manage.py", "migrate", "--no-input"]
