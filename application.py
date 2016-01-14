import re
from response import *

urls = (
          ("/","root"),
          ("/hello","hello"),
          ("/index","index"),
       )

'''
wsgi application type is function
'''
def def_my_app(environ,start_response):
    status200 = '200 OK'
    status404 = '404 NOT FOUND'
    respheader = [('Content-type','text/plain')]
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    for pattern, name in urls:
        m = re.match('^' + pattern + '$', path)
        if m:
            args = m.groups()
            funcname = method.upper()
            klass = globals().get(name.upper())
            if hasattr(klass,funcname):
                func = getattr(klass,funcname)
                start_response(status200,respheader)
                return func(klass(),*args)
    else:
        start_response(status404,respheader)
        return "404 NOT FOUND\n"

'''
wsgi application type is class
'''
class class_my_app(object):
    def __init__(self,environ,start_response):
        self.environ = environ
        self.start_response = start_response
        self.urls = urls
        self.respheader = [('Content-type','text/plain')]
        self._status = '200 OK'
    def __iter__(self):
        result = self.delegate()
        self.start_response(self._status,self.respheader)

        if isinstance(result,basestring):
            return iter([result])
        else:
            return iter(result)
    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                args = m.groups()
                funcname = method.upper()
                klass = globals().get(name.upper())
                if hasattr(klass,funcname):
                    func = getattr(klass,funcname)
                    self._status = '200 OK'
                    return func(klass(),*args)

        return self.notfound()
    def notfound(self):
        self._status = '404 NOT FOUND'
        return "404 NOT FOUND\n"
