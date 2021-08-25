from sqlalchemy.sql.expression import bindparam
import tornado.web
import tornado.websocket
from tornado.escape import json_decode
from tornado_sqlalchemy import SessionMixin

from .models import db, Project
from .constants import API_PREFIX, UPLOAD_FOLDER
from . import projects 
from . import storage
from . import annotator


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers","X-Requested-With")


class ProjectHandler(SessionMixin, BaseHandler):
    def get(self):
        with self.make_session() as session:
            self.write({
                "results" : projects.get_all(session)
            })

    def post(self, action):
        if action == "new":
            return self.new_project()
        if action == "check":
            return self.check_project()
        return self.write("No match")

    def new_project(self):
        req = json_decode(self.request.body)
        with self.make_session() as session:
            projects.add(session, req)

    def check_project(self):
        pass

        


class FileStorageHandler(SessionMixin, BaseHandler):
    def get(self,path):
        with self.make_session() as session:
            content_type, binary_data = storage.get(session, path)
        self.add_header('Content-Type', content_type)
        self.write(binary_data)
        
        

class FileUploadHandler(SessionMixin, BaseHandler):
    def post(self):
        file =  self.request.files["fileupload"][0]
        with self.make_session() as session:
            self.write(storage.add(session, file))



class AnnotatorHandler(SessionMixin, tornado.websocket.WebSocketHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def open(self):
        print("Websocket opened")

    def on_message(self, message):
        msg = json_decode(message)
        with self.make_session() as session:
            resp = annotator.read_message(session, msg)
        self.write_message(resp)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self,origin):
        return "localhost" in origin

handlers = [
        (r"/upload", FileUploadHandler),
        (r"/storage/(.*)",FileStorageHandler),
        (r"/projects", ProjectHandler),
        (r"/projects/(.*)", ProjectHandler),
        (r"/annotate", AnnotatorHandler)
    ]