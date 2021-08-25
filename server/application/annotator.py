from uuid import uuid4
from .models import Casestudy, Project, Source, Label

def read_message(session, message):
    print(message)
    if message["event"] == 'validate':
        return validate(session, message)

def validate(session, message):
    """"Validates the project id
    """
    if session.query(Project).filter_by(uid=message["data"]).first():
        return {"event" : "validated"}
    return {"event" : "invalidated"}