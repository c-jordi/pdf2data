import re
from uuid import uuid4
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type
from pathlib import Path

from .models import Source
from .constants import ROOT, UPLOAD_FOLDER
from . import tasks


def add(session, file):
    """Adds file to storage.

    Args:
        session :
        file : object
            File object
    """
    filename, body, content_type = file["filename"], file["body"], file["content_type"]
    uid = uuid4().hex
    fname = uid + Path(filename).suffix
    uri = ROOT + UPLOAD_FOLDER + fname

    with open("application/" + UPLOAD_FOLDER + fname, 'wb') as f:
        f.write(body)

    preproc_id = preprocess(uid, uri)

    new_source = Source(uid=uid, filename=filename,
                        uri=uri, preproc_id=preproc_id)
    session.add(new_source)
    session.commit()

    return {
        'URI': uri,
        'size': str(len(body) / 1e6) + "MB",
        'filename': filename,
        'uid': uid
    }


def preprocess(uid, uri):
    """Async preprocess file after upload.

    Args:
        uri : (str)
    """
    task = tasks.process_pdf.delay(uid, uri)
    return task.id


def update(session, uid, data):
    """Update source file.

    Args:
        session 
        uid : (str) unique identifier of the source file
        data : (object)
    """
    source = session.query(Source).filter_by(uid=uid)
    source.update(data)


def get(path):
    """Gets file from storage.

    Returns:
        (content_type, binary_data)
    """
    file_location = join("application/"+UPLOAD_FOLDER, path)
    if not isfile(file_location):
        raise HTTPError(status_code=404)
    content_type, _ = guess_type(file_location)
    with open(file_location, "rb") as source_file:
        return (content_type, source_file.read())
