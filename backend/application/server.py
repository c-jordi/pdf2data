import uuid
import tornado.ioloop
import tornado.web
from tornado import options
import sqlite3
import logging
from mimetypes import guess_type
from uuid import uuid4
from os.path import splitext, isfile

__UPLOADS__ = "storage/"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers","X-Requested-With")


class FileUploadHandler(BaseHandler):
    def post(self):
        
        info =  self.request.files["fileupload"][0]
        filename, body, content_type = info["filename"], info["body"], info["content_type"]
        logging.info(
            'POST "%s" "%s" %d bytes', filename, content_type, len(body)
        )
        fname = uuid4().hex + "_" + filename
        with open(__UPLOADS__+ fname, 'wb') as f:
            f.write(body)

        self.write({
            'URI': 'http://0.0.0.0:8888/' + __UPLOADS__ + fname, 
            'size' : str(len(body) / 1e6) + "MB",
            'filename' : filename
            })

class FileStorageHandler(BaseHandler):
    def get(self,path):
        file_location =  __UPLOADS__ + path;
        if not isfile(file_location):
            raise tornado.web.HTTPError(status_code=404)
        content_type, _ = guess_type(file_location)
        self.add_header('Content-Type', content_type)
        with open(file_location, "rb") as source_file:
            self.write(source_file.read())


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", FileUploadHandler),
        (r"/storage/(.*)",FileStorageHandler)
    ],debug=True)


if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(8888)
    print("Running the server at 0.0.0.0:8888")
    tornado.ioloop.IOLoop.current().start()
