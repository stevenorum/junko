#!/usr/bin/env python

import json

class blob(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__predefined_attributes__ = [a for a in dir(self)]
        self.__predefined_attributes__.append("__predefined_attributes__")
        for key in self.keys():
            if not key in self.__predefined_attributes__:
                setattr(self, key, self[key])
                pass
            pass
        pass

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if not key in self.__predefined_attributes__:
            setattr(self, key, self[key])
            pass
        pass

    def __delitem__(self, key):
        super().__delitem__(key)
        if not key in self.__predefined_attributes__:
            delattr(self, key)
            pass
        pass

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

def dumpf(obj, filename, *args, **kwargs):
    with open(filename, "w") as f:
        return json.dump(obj, f, *args, **kwargs)

def load(*args, **kwargs):
    return json.load(*args, **kwargs)

def loads(*args, **kwargs):
    return json.loads(*args, **kwargs)

def loadf(filename, *args, **kwargs):
    with open(filename, "r") as f:
        return json.load(f, *args, **kwargs)
