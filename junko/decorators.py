#!/usr/bin/env python3

import base64
from functools import update_wrapper
from junko import logster
from junko import kson as json
from junko.random_utils import to_object, minify_json
from junko.exceptions import HttpError
from junko.response_core import make_response

import logging
from traceback import format_exc

# def api_call(function):
#     def newfunc(request):
#         body = request.get("body",None)
#         body = body if body else {}
#         kwargs = json.loads(body) if isinstance(body, str) else body
#         if request.get("queryStringParameters", None):
#             kwargs.update(request["queryStringParameters"])
#         return function(raw_request=request, **kwargs)
#     update_wrapper(newfunc, function)
#     return newfunc

def api_call(*args, **kwargs):
    if args:
        return _api_call()(args[0])
    return _api_call(**kwargs)

def _api_call(unpack_body=True):
    def wrapper(function):
        def newfunc(request):
            print(json.dumps(request, indent=2, sort_keys=True))
            user_params = request.get("queryStringParameters", None)
            user_params = user_params if user_params else {}
            body = request.get("body", None)
            params = {"_request":request}
            if body:
                print("Body:")
                print(body)
                if request.get("isBase64Encoded", False):
                    body = base64.b64decode(body.encode("utf-8"))
                if unpack_body:
                    body = body.decode("utf-8") if isinstance(body, bytes) else body
                    user_params.update(json.loads(body))
            params["_body"] = body
            params.update(user_params)
            try:
                return function(**params)
            except HttpError as e:
                return e.response()
            except Exception as e:
                logging.error(format_exc())
                return make_response(body='Internal server error.', code=500)
        update_wrapper(newfunc, function)
        return newfunc
    return wrapper

def log_calls(function):
    def newfunc(*args, **kwargs):
        try:
            #print(str(args))
            #print(str(kwargs))
            event = to_object(kwargs.get("event", args[0]))
            identity = event["requestContext"]["identity"]
            call = {}
            call["ip"] = identity["sourceIp"]
            call["agent"] = identity["userAgent"]
            call["path"] = event["path"]
            call["body"] = event["body"]
            call["referer"] = event.get("headers",{}).get("Referer",None)
            logster.info(minify_json(call))
        except:
            logster.error("Unable to properly log call {event}".format(event=str(args)))
        return function(*args, **kwargs)
    update_wrapper(newfunc, function)
    return newfunc

def log_trace(function):
    def newfunc(*args, **kwargs):
        logster.trace("Entering function {name} with args {args} and kwargs {kwargs}.".format(name=function.__name__, args=args, kwargs=kwargs), trace_depth=1)
        try:
            return function(*args, **kwargs)
        finally:
            logster.trace("Leaving function {name}".format(name=function.__name__), trace_depth=1)
    update_wrapper(newfunc, function)
    return newfunc

def log_errors(function):
    def newfunc(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            logster.error("Error encountered:")
            logster.error(format_exc())
            raise
    update_wrapper(newfunc, function)
    return newfunc

def redirect_errors(destination):
    def newfunc1(function):
        def newfunc2(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except:
                return destination
        return newfunc2
    update_wrapper(newfunc, function)
    return newfunc1
