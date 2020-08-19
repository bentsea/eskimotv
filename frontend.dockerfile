#FROM python:3.8.1-alpine3.11
#RUN apk update && apk upgrade && apk add bash && apk add dumb-init libsass sassc
#RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev

FROM python:3.8.1-slim
#Update and upgrade.
RUN apt-get update && apt-get upgrade -y
#Add sass interpreter.
RUN apt-get install sassc -y
#Add dependency for installing flaskfilemanager
RUN apt-get install swig build-essential -y

#Set ENV Variables
ENV LIBRARY_PATH=/lib:/usr/lib

#Add user.
#RUN adduser -D eskimotv
RUN adduser eskimotv
USER eskimotv

#Set Work directory
WORKDIR /home/eskimotv

#Install Dependencies
COPY requirements app/requirements
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r app/requirements/docker.txt

#Copy project files
COPY app app/app
COPY migrations app/migrations
COPY boot.sh ./app/

#Deploy Project
EXPOSE 5000
#This is now being done in the docker compose file.
#ENTRYPOINT ["./boot.sh"]
