#!?usr/bin/env python3

from junko import kson as json
from junko import logster
from junko.random_utils import *
import os

_sunyata_config = {}

def sunyata_config():
    global _sunyata_config
    if not _sunyata_config:
        with open(os.path.join(os.environ['LAMBDA_TASK_ROOT'],"sunyata.json"), "r") as f:
            _sunyata_config = json.load(f)
            pass
        if _sunyata_config.get("static_file_bucket", None):
            _sunyata_config["static_base_path"] = "https://s3.amazonaws.com/" + _sunyata_config["static_file_bucket"] + "/"
            pass
        _sunyata_config["debug_enabled"] = True if _sunyata_config.get("debug_enabled", False) else False
        _sunyata_config["whitelist_code"] = _sunyata_config.get("whitelist_code", None)
        _sunyata_config["template_dir"] = os.path.join(os.environ['LAMBDA_TASK_ROOT'], "templates")
        if not _sunyata_config["base_url"].startswith("http"):
            _sunyata_config["base_url"] = "https://" + _sunyata_config["base_url"]
        _sunyata_config["base_url_w_slash"] = add_trailing_slash(_sunyata_config["base_url"])
        _sunyata_config["base_url_wo_slash"] = strip_trailing_slash(_sunyata_config["base_url"])
        pass
    return json.blob(_sunyata_config)

SUNYATA_CONFIG = sunyata_config()
