import json
from sqlalchemy.sql.expression import bindparam
import tornado.web
import tornado.websocket
from tornado.escape import json_decode
from tornado_sqlalchemy import SessionMixin

from .models import db, Project
from .constants import API_PREFIX, UPLOAD_FOLDER, API_AUTH
from .schemas import SchemaError, project_req_schema, project_upd_schema
from . import projects
from . import storage
from . import feat_extract
from . import annotator
from . import search


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")


class StatusHandler(BaseHandler):
    def get(self):
        return self.write("The server is running!")


class ProjectHandler(SessionMixin, BaseHandler):
    def get(self, uid=''):
        with self.make_session() as session:
            if uid == '':
                self.write({
                    "results": projects.get_all(session)
                })
            else:
                self.write(projects.get(session, uid))

    async def post(self, action):
        if action == "update":
            return self.update_project()
        if action == "new":
            return self.new_project()
        if action == "check":
            return self.check_project()
        return self.write("No match")

    def new_project(self):
        req = json_decode(self.request.body)
        try:
            project_req_schema.validate(req)
            with self.make_session() as session:
                projects.add(session, req)
        except SchemaError as e:
            raise e

    def update_project(self):
        req = json_decode(self.request.body)
        try:
            project_upd_schema.validate(req)
            with self.make_session() as session:
                projects.update(session, req)
        except SchemaError as e:
            raise e

    def check_project(self):
        pass


class FileStorageHandler(SessionMixin, BaseHandler):
    def get(self, path):
        print("path:", path)
        with self.make_session() as session:
            content_type, binary_data = storage.get(path)
        self.add_header('Content-Type', content_type)
        self.write(binary_data)

    def post(self):
        file = self.request.files["fileupload"][0]
        with self.make_session() as session:
            self.write(storage.upload(session, file))


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

    def check_origin(self, origin):
        return "localhost" in origin


class TaskHandler(SessionMixin, BaseHandler):
    def post(self, task_name):
        token = self.request.headers.get("Token")
        if token != API_AUTH:
            return 401

        if task_name == "save_xml":
            data = json_decode(self.request.body)
            file_info = {"filename": data["data"]["filename"], "body": data["data"]["body"],
                         "content_type": data["data"]["content_type"]}
            with self.make_session() as session:
                storage.add_xml(session, data['uid'], file_info)
            print("XML file has been saved.")

        if task_name == "save_features":
            data = json_decode(self.request.body)
            file_info = data["data"]
            with self.make_session() as session:
                feat_extract.save_features(session, data["uid"], file_info)
            print("Features saved in the DB table.")


class SearchHandler(SessionMixin, BaseHandler):
    def post(self):
        data = json_decode(self.request.body)
        with self.make_session() as session:
            results = search.run(session, data)
        self.write({
            "suggestions": results
        })


class SyncHandler(SessionMixin, BaseHandler):
    def post(self, level, uid):
        data = json_decode(self.request.body)
        with self.make_session() as session:
            results = search.run(session, data)
        self.write({
            "suggestions": results
        })


handlers = [
    (r"/", StatusHandler),
    (r"/upload", FileStorageHandler),
    (r"/storage/(.*)", FileStorageHandler),
    (r"/projects/(.*)", ProjectHandler),
    (r"/projects", ProjectHandler),
    (r"/annotate", AnnotatorHandler),
    (r"/tasks/([a-zA-Z_]*)", TaskHandler),
    (r"/search", SearchHandler),
]
