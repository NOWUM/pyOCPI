FROM python:3.8-slim
RUN pip install --no-cache-dir gunicorn
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -s /bin/bash admin

USER admin
WORKDIR /app
COPY . /app
VOLUME /data
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --chdir=./ --worker-tmp-dir /dev/shm --workers=2 --threads=2 --worker-class=gthread"
EXPOSE 8000

CMD ["gunicorn", "main:app"]
