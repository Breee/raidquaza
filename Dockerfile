FROM python:3.7-alpine

# Working directory for the application
WORKDIR /usr/src/app
COPY raidquaza /usr/src/app
# prepare to run bot.

#RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN echo "http://mirror.leaseweb.com/alpine/edge/testing" >> /etc/apk/repositories
RUN apk --no-cache update && apk add gcc musl-dev linux-headers geos-dev python3-dev git

RUN cd /usr/src/app && python3 -m pip install -U -r requirements.txt

# Set Entrypoint with hard-coded options
ENTRYPOINT ["python3"]
CMD ["./start_bot.py"]

