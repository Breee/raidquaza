FROM python:3.7-slim

# Working directory for the application
WORKDIR /usr/src/app
COPY raidquaza /usr/src/app
# prepare to run bot.
RUN apt-get update && apt-get install -y supervisor git
RUN mkdir -p /var/log/supervisor
RUN touch /var/run/supervisor.sock && chmod 777 /var/run/supervisor.sock
RUN cd /usr/src/app && pip install -U -r requirements.txt
COPY supervisord.conf /
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]