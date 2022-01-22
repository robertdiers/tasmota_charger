FROM debian:stable-slim

RUN apt update
RUN apt -y upgrade
RUN apt -y install cron python3 python3-pip
RUN pip3 install configparser pymodbus graphyte

# copy files
COPY tasmotacharger.py /app/tasmotacharger.py
COPY tasmotacharger.ini /app/tasmotacharger.ini
COPY tasmotachargerdefaults.ini /app/tasmotachargerdefaults.ini
COPY tasmotacharger.sh /app/tasmotacharger.sh
COPY entrypoint.sh /app/entrypoint.sh
COPY container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]
