#!/bin/bash

# TODO: fetch static db files from network into survey dir

monetdbd start /data

sleep 5
if [ ! -d "/data/survey" ]; then
    monetdb create survey && \
    monetdb set embedr=true survey && \
    monetdb set embedpy=true survey && \
    monetdb release survey
else
    echo "Existing database found in '/data/survey'"
fi

for i in {30..0}; do
    echo 'Testing MonetDB connection ' $i
    mclient -d survey -s 'SELECT 1' &> /dev/null
    if [ $? -ne 0 ] ; then
      echo 'Waiting for MonetDB to start...'
      sleep 1
    else
        echo 'MonetDB is running'
        break
    fi
done
if [ $i -eq 0 ]; then
    echo >&2 'MonetDB startup failed'
    exit 1
fi

# TODO: monetdb set readonly=yes survey
