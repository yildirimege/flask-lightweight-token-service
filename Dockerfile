FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY constants constants
COPY unit_tests unit_tests
COPY database database
COPY utils utils
COPY controller.py controller.py
COPY router.py router.py
COPY settings.py settings.py

#TODO: Add constants such as PostgreSQL Credentials etc. here.

ENV LOG_LEVEL="DEBUG"

ENV POSTGRESQL_CONN_PORT="5432"
ENV POSTGRESQL_DB_NAME="postgres"
ENV POSTGRESQL_TABLE_NAME="flask_identity_provider"
ENV POSTGRESQL_HOST="127.0.0.1"
ENV POSTGRESQL_USERNAME="yildirimege"
ENV POSTGRESQL_PASSWORD="123456"
ENV POSTGRESQL_SSL_MODE="require"

CMD ["gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "--bind", "0.0.0.0:8080", "--preload", "router:flask_app"]

EXPOSE 8080