FROM python:3.7-alpine

# Working directory for the application
WORKDIR /usr/src/app
COPY raidquaza /usr/src/app
# prepare to run bot.
RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update && apk add --no-cache gcc python3-dev musl-dev linux-headers supervisor git geos-dev@testing
RUN mkdir -p /var/log/supervisor
RUN touch /var/run/supervisor.sock && chmod 777 /var/run/supervisor.sock
RUN cd /usr/src/app && python3 -m pip install -U -r requirements.txt
COPY supervisord.conf /
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
