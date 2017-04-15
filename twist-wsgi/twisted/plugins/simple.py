from __future__ import absolute_import

import os

from zope import interface

from twisted.python import usage, reflect, threadpool, filepath
from twisted import plugin
from twisted.application import service, strports, internet
from twisted.web import wsgi, server, static, resource
from twisted.internet import reactor

import twemo.wsgi

class Options(usage.Options):
    optParameters = [["port", None, None, "strports description of the port to "
                      "start the server on."],
                    ]

class DelegatingResource(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, name, request):
        request.prepath = []
        request.postpath.insert(0, name)
        return self.wsgi_resource

@interface.implementer(service.IServiceMaker, plugin.IPlugin)
class ServiceMaker(object):
    tapname = "simple"
    description = "Simple"
    options = Options

    def makeService(self, options):
        application = twemo.wsgi.application
        pool = threadpool.ThreadPool()
        reactor.callWhenRunning(pool.start)
        reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
        wsgi_resource = wsgi.WSGIResource(reactor, pool, application)
        static_resource = static.File('.')
        root = DelegatingResource(wsgi_resource)
        root.putChild('static', static_resource)
        site = server.Site(root)
        ret = strports.service(options['port'], site)
        return ret

serviceMaker = ServiceMaker()
