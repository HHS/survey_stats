#!/bin/bash

# TODO: fetch static db files from network into survey dir
monetdbd start /home/monetdb

sleep 5
if [ ! -d "/home/monetdb/survey" ]; then
    monetdb create survey && \
    monetdb set embedr=true survey && \
    monetdb set embedpy=true survey && \
    monetdb release survey
else
    echo "Existing database found in '/home/monetdb/survey'"
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

$STATS_LOCK='.survey.lock'

if [ ! -f $STATS_LOCK ]; then
    echo "Fetching data files for survey db..."
    curl -O "https://s3.amazonaws.com/cdc-survey-data/survey_data-07Sep2017.tar.gz"
    tar -xzf survey_data-07Sep2017.tar.gz
    SQLF=./survey_data/*.sql
    for f in $SQLF
    do
        mclient -d survey $f
    done
    touch $STATS_LOCK
fi


# TODO: monetdb set readonly=yes survey
