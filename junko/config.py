#!?usr/bin/env python3

from junko import kson as json
from junko import logster
from junko.random_utils import *
import os

_sunyata_config = {}

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

def sunyata_config():
    global _sunyata_config
    if not _sunyata_config:
        with open(os.path.join(os.environ['LAMBDA_TASK_ROOT'],"sunyata.json"), "r") as f:
            _sunyata_config = json.load(f)
            pass
        _sunyata_config["static_base_path"] = "https://s3.amazonaws.com/" + _sunyata_config["static_file_bucket"] + "/"
        _sunyata_config["debug_enabled"] = True if _sunyata_config.get("debug_enabled", False) else False
        _sunyata_config["whitelist_code"] = _sunyata_config.get("whitelist_code", None)
        _sunyata_config["template_dir"] = os.path.join(os.environ['LAMBDA_TASK_ROOT'], "templates")
        if not _sunyata_config["base_url"].startswith("http"):
            _sunyata_config["base_url"] = "https://" + _sunyata_config["base_url"]
        pass
    return blob(_sunyata_config)

SUNYATA_CONFIG = sunyata_config()
