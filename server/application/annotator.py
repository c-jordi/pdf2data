from uuid import uuid4
from .models import Casestudy, Project, Source, Label
from .temp import test_img_url


def read_message(session, message):
    print(message)
    if message["event"] == 'validate':
        return validate(session, message)
    if message["event"] == 'load':
        return {"event": "update", "data":
                [
                    {"type": "image", "id": "img-0", "data": {
                        "src": test_img_url
                    }
                    },
                    {"type": "annotations", "id": "ann-0", "data": [
                        {"bbox": [100, 100, 300, 300],
                         "label": "Title", "color": "purple"},
                        {"bbox": [200, 200, 400, 300],
                         "label": "Speech", "color": "blue"}
                    ]
                    }

                ]

                }


def validate(session, message):
    """"Validates the project id
    """
    if session.query(Project).filter_by(uid=message["data"]).first():
        return {"event": "validated"}
    return {"event": "invalidated"}
