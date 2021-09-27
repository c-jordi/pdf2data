from application.server import make_app
import tornado
import os

BACKEND_PORT = os.environ.get("BACKEND_PORT", 8888)

app = make_app()
app.listen(BACKEND_PORT)

print(f"Running the server at 0.0.0.0:{BACKEND_PORT}")
tornado.ioloop.IOLoop.current().start()
