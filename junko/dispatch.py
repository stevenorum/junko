#!/usr/bin/env python3

from junko.formatting import format_content
from junko.response_core import *
from junko.random_utils import *
import re
from urllib.parse import urljoin

class Dispatcher(object):
    def __init__(self):
        pass

    pass

class Link(Dispatcher):
    path = None
    def __init__(self, path, handler=None, debug_name="Link"):
        self.path = path if isinstance(path, str) else path.pattern
        self.compiled_path = re.compile(path) if isinstance(path, str) else path
        self.handle = handler if handler else self._default_handler
        self.debug_name = debug_name
        pass

    def dispatch(self, request):
        if (self.compiled_path.match(request.get("path", None))):
            return self.handle(request)
        else:
            return None
        pass

    def _default_handler(self, request):
        return None

    def debug_info(self):
        return "{} ({})".format(getattr(self,'path'), self.debug_name)
    
    pass

class DispatchChain(Dispatcher):
    def __init__(self, *dispatchers, **kwargs):
        self.path = None
        self.debug_name = kwargs.get('debug_name', "DispatchChain")
        if dispatchers and isinstance(dispatchers[0], str):
            self.debug_name = dispatchers[0]
            dispatchers = dispatchers[1:]
        self.dispatchers = [d for d in dispatchers]
        pass

    def add_link(self, dispatcher):
        if hasattr(dispatcher, 'path'):
            self.remove_link(dispatcher.path)
        self.dispatchers.append(dispatcher)
        pass

    def add_links(self, *dispatchers):
        for dispatcher in dispatchers:
            self.add_link(dispatcher)
            pass
        pass

    def remove_link(self, path):
        for i in range(len(self.dispatchers)):
            dispatcher = self.dispatchers[i]
            if path == getattr(dispatcher, 'path'):
                del self.dispatchers[i]
                return
            pass
        pass

    def dispatch(self, request):
        for dispatcher in self.dispatchers:
            response = dispatcher.dispatch(request)
            if response:
                return response
            pass
        return None

    def debug_info(self):
        return {self.debug_name: [d.debug_info() for d in self.dispatchers]}
    pass

class MessageLink(Link):
    def __init__(self, path, message, title="", format_message=True, debug_name="MessageLink"):
        super().__init__(
            path=path,
            handler=respond_with(
                make_response(
                    "<html><head><title>{title}</title></head><body>{body}</body></html>".format(
                        body=format_content(message) if format_message else message,
                        title=title
                    )
                )
            ),
            debug_name=debug_name
        )
        pass
    pass

class RedirectLink(Link):
    def __init__(self, path, target_url, unrelativize_link=True, temporary=True, debug_name="RedirectLink"):
        super().__init__(
            path=path,
            handler=respond_with(
                create_redirect_response(
                    target_url=target_url,
                    unrelativize_link=unrelativize_link,
                    temporary=temporary
                )
            ),
            debug_name=debug_name
        )
        pass
    pass

class StaticLink(RedirectLink):
    def __init__(self, filename, path=None, debug_name="StaticLink"):
        super().__init__(
            path=path if path else re.escape(add_leading_slash(filename)),
            target_url=static_path(filename),
            temporary=True,
            debug_name=debug_name
        )
        pass
    pass
