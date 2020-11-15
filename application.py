import os
import tornado.web
import config
from view import index


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [

            (r'/demo', index.DemoHandler),

            # 主页
            (r'/main', index.MainPageHandler),

            # 上传文件
            (r'/upfile', index.UpFileHandler),

            # 展示文件内容
            (r'/filelist', index.GetFileListHandler),



            # StaticFileHandler,注意要放在所有路由的最下面
            (r'/(.*)$', index.StaticFileHandler, {"path": os.path.join(config.BASE_DIRS, 'static/html'), \
                                                  "default_filename": "main.html"}),
        ]

        super(Application, self).__init__(handlers, **config.settings)
        print('Tornado backend server starting....')
        print('listening on port ', config.options['port'])
