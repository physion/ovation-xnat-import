'''
Copyright (c) 2012 Physion Consulting, LLC
'''

__author__ = 'barry'

import time

def xnat_api(fn, *args, **kwargs):
    xnat_api_pause()
    return fn(*args, **kwargs)



def xnat_api_pause():
    time.sleep(1)

def iterate_entity_collection(fn):
    for e in fn():
        xnat_api_pause()
        yield e
