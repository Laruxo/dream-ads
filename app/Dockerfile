FROM python:latest

WORKDIR /var/www
COPY requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
