#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
#substitutes all the syntax preceded by a dollar sign with the env variable with that name
nginx -g 'daemon off;'

#And all that means is that we want to run  nginx in the foreground.

#It is the primary thing being run by that Docker container and this way all of the logs and everything

#get output to the screen and the Docker container will continue to run while the engine x server is

#running.
