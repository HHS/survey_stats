#!/bin/bash

curl -O "https://s3.amazonaws.com/cdc-survey-data/versions/1.0.0/cache.tgz" && \
    rm -rf cache && \
    tar -xvzf cache.tgz && \
    pip install -e .
