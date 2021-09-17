from application.server import make_app
import tornado

app = make_app()
app.listen(8888)
print("Running the server at 0.0.0.0:8888")
tornado.ioloop.IOLoop.current().start()
