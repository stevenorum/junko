#!/usr/bin/env python3

from junko.config import SUNYATA_CONFIG
from junko.random_utils import *

import datetime
from urllib.parse import urljoin

def unrelativize(url):
    if url.startswith("https://") or url.startswith("http://"):
        return url
    return urljoin(add_trailing_slash(SUNYATA_CONFIG.base_url), strip_leading_slash(url))

def static_path(filename):
    return "https://s3.amazonaws.com/" + SUNYATA_CONFIG.static_file_bucket + add_leading_slash(filename)

def make_response(body, code=200, headers={"Content-Type": "text/html"}):
    return {
        "body": body,
        "statusCode": code,
        "headers": headers
    }

def respond_with(response):
    return lambda *args, **kwargs: response

def unrelativize(url):
    return urljoin(add_trailing_slash(SUNYATA_CONFIG.base_url), strip_leading_slash(url))

def create_redirect_response(target_url, unrelativize_link=True, temporary=True):
    return make_response(
        body = "",
        code = 303 if temporary else 301,
        headers = {"Location": unrelativize(target_url) if unrelativize_link else target_url}
    )

def add_cookie(response, key, value, seconds=0, minutes=0, hours=0, days=0):
    expires = (datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    return set_cookie(response, key=key, value=value, expires=expires, domain=get_domain(SUNYATA_CONFIG["base_url"]))

def delete_cookie(response, key):
    return set_cookie(response, key=key, value="", expires=datetime.datetime.utcfromtimestamp(123).strftime("%a, %d %b %Y %H:%M:%S GMT"), domain=get_domain(SUNYATA_CONFIG["base_url"]), path="/")

def set_cookie(response, key, value, expires, **kwargs):
    cookie = "{key}={value};".format(key=key, value=value)
    cookie += "expires={expires};".format(expires=expires)
    for k in kwargs:
        cookie += "{key}={value};".format(key=k, value=kwargs[k])
    new_key = find_unused_casing("set-cookie", [k for k in response["headers"].keys() if k.lower() == "set-cookie"])
    # TODO LOPRI: add error handling for when this tries to set more cookies than there are valid case alterations.
    response["headers"][new_key] = cookie
    return response

def get_cookies(event):
    # TODO MOPRI: make this safer or smarter about malformed strings.
    return parse_cookie_string(to_object(event)["headers"].get("Cookie", ""))

def parse_cookie_string(s):
    return {c.split("=")[0]:"=".join(c.split("=")[1:]) if len(c.split("=")) > 1 else True for c in s.split("; ") if c} if s else {}
