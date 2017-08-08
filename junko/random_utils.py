#!/usr/bin/env python3

from junko import kson as json
import math
from urllib.parse import urlparse

content_types = {
    "jpg":"image/jpg",
    "jpeg":"image/jpeg",
    "png":"image/png",
    "gif":"image/gif",
    "bmp":"image/bmp",
    "tiff":"image/tiff",
    "txt":"text/plain",
    "rtf":"application/rtf",
    "ttf":"font/ttf",
    "css":"text/css",
    "html":"text/html",
    "js":"application/javascript",
    "eot":"application/vnd.ms-fontobject",
    "svg":"image/svg+xml",
    "woff":"application/x-font-woff",
    "woff2":"application/x-font-woff",
    "otf":"application/x-font-otf",
    "json":"application/json",
    }

def get_content_type(fname, body):
    return content_types.get(fname.split(".")[-1].lower(),"binary/octet-stream")

def to_object(inp):
    if not inp:
        return {}
    if type(inp) == str:
        try:
            return json.loads(inp)
        except Exception as e:
            raise RuntimeError("Error handling string '{}' : {}".format(inp, e))
    return inp

def pull_attrs(d, attrs):
    pulled = {}
    for attr in attrs:
        pulled[attr] = d.get(attr, None)
    return pulled

def minify_json(_json):
    return json.dumps(to_object(_json), sort_keys=True, separators=(',',':'))

def apply_mask(list_of_stuff, mask, zero, one):
    masked_stuff = [one(list_of_stuff[i]) if mask[i%len(list_of_stuff)]=="1" else zero(list_of_stuff[i]) for i in range(len(list_of_stuff))]
    if type(list_of_stuff) == str:
        return "".join(masked_stuff)
    return masked_stuff

def apply_case_mask(phrase, mask, invert=False):
    if type(phrase) == str:
        UPPER = str.upper
        LOWER = str.lower
    if invert:
        return apply_mask(phrase, mask, zero=UPPER, one=LOWER)
    else:
        return apply_mask(phrase, mask, zero=LOWER, one=UPPER)

def find_unused_casing(phrase, existing=[]):
    letter_locations = [i for i in range(len(phrase)) if phrase[i].isalpha()]
    letter_count = len(letter_locations)
    try:
        xrange(1)
    except:
        xrange = range
    for i in xrange(int(math.pow(2,letter_count))):
        mask = [c for c in "{0:b}".format(i).zfill(letter_count)]
        expand_mask_list = [mask.pop() if i in letter_locations else phrase[i] for i in range(len(phrase))]
        mask = "".join(expand_mask_list) if type(phrase) == str else u"".join(expand_mask_list)
        masked_phrase = apply_case_mask(phrase, mask)
        if not masked_phrase in existing:
            return masked_phrase
    return None

def get_domain(url):
    return urlparse(url).netloc

def strip_trailing_slash(s):
    if not s or not s[-1] == "/":
        return s
    else:
        return strip_trailing_slash(s[:-1])

def add_trailing_slash(s):
    if not s or not s[-1] == "/":
        return "{s}/".format(s=s)
    else:
        return s

def strip_leading_slash(s):
    if not s or not s[0] == "/":
        return s
    else:
        return s[1:]

def add_leading_slash(s):
    if not s or not s[0] == "/":
        return "/{s}".format(s=s)
    else:
        return s
