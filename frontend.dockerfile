FROM python:3.8.1-alpine3.11
RUN apk update && apk upgrade && apk add bash && apk add dumb-init libsass sassc
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev

#Set ENV Variables
ENV LIBRARY_PATH=/lib:/usr/lib

#Add user.
RUN adduser -D eskimotv
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
#ENTRYPOINT ["./boot.sh"]
