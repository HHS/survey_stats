#!/bin/bash

# TODO: fetch static db files from network into survey dir

sleep 5
if [ ! -d "/var/monetdb5/dbfarm/survey" ]; then
    monetdb create survey && \
    monetdb set embedr=true survey && \
    monetdb set embedpy=true survey && \
    monetdb release survey
else
    echo "Existing database found in '/var/monetdb5/dbfarm/survey'"
fi

# TODO: monetdb set readonly=yes survey
