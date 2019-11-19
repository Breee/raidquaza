FROM python:3.7-slim

# Working directory for the application
WORKDIR /usr/src/app
COPY raidquaza /usr/src/app
# prepare to run bot.

RUN apt update && apt install -y git

RUN cd /usr/src/app && python3 -m pip install -U -r requirements.txt

# Set Entrypoint with hard-coded options
ENTRYPOINT ["python3"]
CMD ["./start_bot.py"]

