FROM python:3.7-alpine

# Working directory for the application
WORKDIR /usr/src/app
COPY raidquaza /usr/src/app
# prepare to run bot.

RUN apk --no-cache update && apk add gcc python3-dev musl-dev linux-headers git
RUN apk add --no-cache \
libc-dev \
geos-dev \
&& pip install shapely

RUN cd /usr/src/app && python3 -m pip install -U -r requirements.txt

# Set Entrypoint with hard-coded options
ENTRYPOINT ["python3"]
CMD ["./start_bot.py"]

