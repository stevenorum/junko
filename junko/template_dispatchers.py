#!/usr/bin/env python3

from junko.config import SUNYATA_CONFIG
from junko.random_utils import add_trailing_slash, strip_trailing_slash
from junko.response_core import make_response
from junko.dispatch import Link

from jinja2 import Environment, FileSystemLoader
import re

env = Environment(loader=FileSystemLoader(SUNYATA_CONFIG.template_dir))

def default_params():
    params = dict(SUNYATA_CONFIG)
    params["base_url_w_slash"] = add_trailing_slash(SUNYATA_CONFIG.base_url)
    params["base_url_wo_slash"] = strip_trailing_slash(SUNYATA_CONFIG.base_url)
    if SUNYATA_CONFIG.get("static_base_path", None):
        params["static_url_w_slash"] = add_trailing_slash(SUNYATA_CONFIG.static_base_path)
        params["static_url_wo_slash"] = strip_trailing_slash(SUNYATA_CONFIG.static_base_path)
    return params

def load_template(template_name, params={}, include_default_params=True, **kwargs):
    template = env.get_template(template_name)
    template_params = default_params() if include_default_params else {}
    template_params.update(params)
    body = template.render(**template_params)
    return make_response(body, **kwargs)

def get_template_handler(template_name, param_loader=None, **kwargs):
    def handle_template(request):
        params = default_params()
        if param_loader:
            try:
                params.update(param_loader(request, params=params))
            except:
                # This was the original version, so fall back to it if necessary.
                params.update(param_loader(request))
            pass
        return load_template(template_name=template_name, params=params, **kwargs)
    return handle_template

class TemplateLink(Link):
    def __init__(self, path, template_name, param_loader=None, debug_name="TemplateLink",**kwargs):
        super().__init__(path, get_template_handler(template_name=template_name, param_loader=param_loader, **kwargs), debug_name=debug_name)
        pass
    pass
