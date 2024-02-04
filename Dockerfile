FROM python:3.9.3-alpine3.13
#alpine is a lightweight versionn for linux (image with bare minimum dependencies )
LABEL maintainer="OnsKouki"
#maintainer is the person/ organisation (website) responsible for maintaining the docker image

ENV PYTHONUNBUFFERED 1
#env variable to not buffer the output -> printed directly to the console (log)
COPY ./requirements.txt /tmp/requirements.txt
#copies the file to the /tmp repo in the docker image ( to use it to install the python requirements)
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
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
    apk add --update --no-cache postgresql-client jpeg-dev &&\
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV= "true"]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir  -p /vol/web/media && \
    mkdir  -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    #chmod a+rwx -R run/ && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

#Run A commands in the alpine image -> one bloc to just keep 1 image layer --> LIGHT-WEIGHT IMAGE,
#1st :to create a virtual env to store dependencies --> to avoid conflicting dependencies in the base image (Optional)
#2nd :upgrade pip in the environment
#3rd :install requirements.txt in the env
  #3rd bis install requirements.dev if dev=true
#4th :remove /tmp to remove extra dependencies --> BEST PRACTICE FOR LIGHT WEIGHT container
#add user (with/ pass or home dir) that doesnt have root privelegs --> BETTER FOR SECURITY

#apk add --update --no-cache postgresql-client &\  -> install the client package inside the alpine image so that psycog2 package connects to postgres
#it is a dependency that needs to stay in prod
#apk add --update --no-cache --virtuam .tmp-build-deps \
#        build-base postgresql-dev musl-dev && \ -> sets a virtual dependency package containing the packages needed to install the postgres adapter
#apk del .tmp-build-deps && \ -> remove them if we are in production
#mkdir -p /vol/web/media and static are the directories where we are going to store the static files in the docker volumes
ENV PATH="/scripts:/py/bin:$PATH"

#create an path env to avoid specifying full path

USER django-user

#run the containers as a django-user (not root)

CMD ["run.sh"]

#default command for docker containers spawn from the image built from the dockerfile
#it runs the script file