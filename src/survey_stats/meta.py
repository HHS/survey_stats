import os
import pandas as pd
import feather
import logging
import numpy as no
import h5py

#TODO: refactor me so that we can load multiple metadata objects

cache_dir = os.path.join(os.getcwd(),'cache')

metaurl = 'data/yrbss_dash.csv.gz'

df = None


class SurveyMetadata(namedtuple('Metadata', ['config','ds'])):
    __slots__ = ()

    @classmethod
    def load_metadata(cls, yml_f):
        config = None
        with open(yml_f, 'r') as fh:
            config = yaml.load(fh)['dash']
        pfx = config['id']
        cachef = os.path.join(cache_dir, pfx + '.h5')
        ds = h5py.File(cachef)
        (qn,df) = (ds['qnmeta'], ds['precomp']) if 'precomp' in ds and \
            'qnmeta' in ds else cls.load_rawmeta(config, ds)
        return cls(config=config, ds=ds)

    @classmethod
    def load_rawmeta(cfg, ds):
        # load dash data
        df = pd.read_csv(cfg['file'][0])
        #TODO: deal with multiple files
        #lowercase col names
        df.columns = df.columns.map(lambda x: x.lower())
        k = cfg['key'] #get the question key
        #rename questions (TODO: cleanup)
        df[k] = df[k].apply( lambda k:
                            k.replace('H','qn') if
                            k[0]=='H' else
                            k.lower())
        #rename columns
        df = df.rename(columns=cfg['rename'])
        ds['qnmeta'] = df[metacols].drop_duplicates().set_index(k)
        ds['precomp'] = df[set(cfg['facet']).union(cfg['strata'], cfg['stats']. [k])]
        return (ds['qnmeta'], ds['precomp'])

