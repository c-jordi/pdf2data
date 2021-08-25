import tornado.ioloop
import tornado.web
from tornado import options

from .handlers import handlers
from .models import db

def make_app():
    db.configure(url='sqlite:///db.sqlite')
    return tornado.web.Application(handlers,debug=True, db=db)

if __name__ == "__main__":
    
    options.parse_command_line()
    app = make_app()
    app.listen(8888)
    print("Running the server at 0.0.0.0:8888")
    tornado.ioloop.IOLoop.current().start()
