FROM python:3.10-slim
RUN pip install --no-cache-dir gunicorn -e .

RUN useradd -s /bin/bash admin

USER admin
WORKDIR /app
COPY . /app
VOLUME /data
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:9000 --chdir=./ --worker-tmp-dir /dev/shm --workers=2 --threads=2 --worker-class=gthread"
EXPOSE 9000

CMD ["gunicorn", "main:app"]
