#!/usr/bin/env python

import json

class JunkoEncoder(json.JSONEncoder):
    def default(self, obj):
        # Let the base class default method raise the TypeError
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return "<unserializable object of type {}>".format(type(obj))

def dump(*args, **kwargs):
    return json.dump(cls=JunkoEncoder, *args, **kwargs)

def dumps(*args, **kwargs):
    return json.dumps(cls=JunkoEncoder, *args, **kwargs)

def load(*args, **kwargs):
    return json.load(*args, **kwargs)

def loads(*args, **kwargs):
    return json.loads(*args, **kwargs)
