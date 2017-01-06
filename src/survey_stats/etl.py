import sys
import os
import boto
import ftplib
import zipfile
from boto.s3.key import Key
import requests
import urllib
import tempfile

combined_dat_files = [
    'https://www.cdc.gov/healthyyouth/data/yrbs/files/sadc_2015_national_ASCII.zip',
    'https://www.cdc.gov/healthyyouth/data/yrbs/files/sadc_2015_state_a_m_ASCII.zip',
    'https://www.cdc.gov/healthyyouth/data/yrbs/files/sadc_2015_state_n_z_ASCII.zip']

with tempfile.TemporaryDirectory() as tmpdir:



