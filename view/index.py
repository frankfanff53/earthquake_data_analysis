from tornado.web import RequestHandler, authenticated
from tornado.httpclient import AsyncHTTPClient
import tornado.web
import config
import os
import Earthquake


class DemoHandler(RequestHandler):
    def get(self):
        self.write("This is a demo!")


class MainPageHandler(RequestHandler):
    def get(self):
        self.render('main.html')


class UpFileHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('upfile.html')

    def post(self):
        file_dict = self.request.files
        for input_name in file_dict:
            file_arr = file_dict[input_name]
            for file_obj in file_arr:
                # 储存路径
                filepath = os.path.join(config.BASE_DIRS, 'upfile/' + file_obj.filename)
                with open(filepath, 'wb') as f:
                    f.write(file_obj.body)
        self.write('success')

        # 或上传成功后直接实现自动跳转到某一页面，如主页
        # self.redirect('/')


class GetFileListHandler(RequestHandler):
    def get(self):
        Earthquake.get_file_list()  # 另外构建一个Earthquake类，调用里面的get_file_list()方法，返回upload目录下所有的地震文件

class FilterEqtCaseHandler(RequestHandler):
    def post(self, ymdOneLimit, abOneSelect, disOneLimit, jingweiLimit):
        # 在Earthquake类内进行筛选震例
        Earthquake.filter_file_list(ymdOneLimit, abOneSelect, disOneLimit, jingweiLimit)

class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
