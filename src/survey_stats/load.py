from survey_stats.etl import download as dl
import filelock

def fetch_data():
    lock = filelock.FileLock('.cache.lock')
    # need to download data and setup db
    logger.info('fetching data cache', url=data_f)
    urllib.request.urlretrieve(data_f, './cache.tar.gz')
    dat = tf.open('cache.tar.gz', mode='r:gz')
    dat.extractall('.')
    logger.info('extracted data cache, now setting up dbs')
    restore_data(dburl)

