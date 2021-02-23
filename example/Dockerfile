FROM python:3.9.1-alpine3.12

# load source code
RUN mkdir /app
COPY example /app
COPY requirements/prod.txt /app/requirements.txt
COPY requirements/db_wrapper-0.1.0a0.tar.gz /app/requirements/db_wrapper-0.1.0a0.tar.gz

VOLUME /app
WORKDIR /app

# install python dependencies
RUN apk add --no-cache --virtual .build-deps \
    # needed to build psycopg2 & yarl
    gcc \
    # needed to build yarl
    musl-dev \
    # needed to build psycopg2
    postgresql-dev \
    # runtime dependency for psycopg2
    && apk add --no-cache libpq \
    # install python packages
    && ls -la requirements \
    && pip install -r requirements.txt \
    # then remove build dependencies
    && apk del .build-deps

# start server
ENTRYPOINT ["python"]
CMD ["example.py"]
