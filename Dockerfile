FROM python:3.8-buster

WORKDIR /usr/src/app

COPY petsrus/semantic_release/ ./petsrus/semantic_release
COPY alembic/ ./
COPY config.py ./
COPY run.py ./
COPY wsgi.py ./
COPY setup.py ./
COPY alembic.ini ./
COPY requirements.txt ./
RUN python setup.py install
COPY petsrus/ ./petsrus/

RUN groupadd -g 3000 pet-group && useradd -m -u 4000 -g pet-group petuser
USER petuser

EXPOSE 5050
CMD [ "--access-logfile", "/home/petuser/petsrus-access.log", "--workers", "3", "--bind", "0.0.0.0:5050", "wsgi:app" ]
ENTRYPOINT ["gunicorn"]
