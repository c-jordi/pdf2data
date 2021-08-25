from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost:5672//')

@app.task
def add(x, y):
    return x + y