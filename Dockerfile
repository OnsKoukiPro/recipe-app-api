FROM python:3.9.3-alpine3.13
#alpine is a lightweight versionn for linux (image with bare minimum dependencies )
LABEL maintainer="OnsKouki"
#maintainer is the person/ organisation (website) responsible for maintaining the docker image 

ENV PYTHONUNBUFFERED 1
#env variable to not buffer the output -> printed directly to the console (log)
COPY ./requirements.txt /tmp/requirements.txt
#copies the file to the /tmp repo in the docker image ( to use it to install the python requirements)
COPY ./requirements.dev.txt /tmp/requirements.dev.txt 

COPY ./app /app
#copies the app repo to the docker image
WORKDIR /app
#default directory where the commands are going to be running from where we run from the docker image
EXPOSE 8000
#to access container via the 8000 port (where we run the django dev server)

ARG DEV=false
#build arg DEV , override it in the yml file when running dev mode (docker-compose)

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV= "true"]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#Run A commands in the alpine image -> one bloc to just keep 1 image layer --> LIGHT-WEIGHT IMAGE, 
#1st :to create a virtual env to store dependencies --> to avoid conflicting dependencies in the base image (Optional)
#2nd :upgrade pip in the environment
#3rd :install requirements.txt in the env
  #3rd bis install requirements.dev if dev=true
#4th :remove /tmp to remove extra dependencies --> BEST PRACTICE FOR LIGHT WEIGHT container
#add user (with/ pass or home dir) that doesnt have root privelegs --> BETTER FOR SECURITY

ENV PATH="/py/bin:$PATH"

#create an path env to avoid specifying full path

USER django-user

#run the containers as a django-user (not root)
