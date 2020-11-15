import config
from application import Application
from tornado import ioloop, httpserver

if __name__ == '__main__':

    app = Application()
    http_server = httpserver.HTTPServer(app)
    http_server.bind(config.options['port'])
    http_server.start(1)
    ioloop.IOLoop.current().start()