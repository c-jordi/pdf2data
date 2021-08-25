from uuid import uuid4
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type

from .models import Source
from .constants import ROOT, UPLOAD_FOLDER


def add(session, file):
    """Adds file to storage.
    
    Args:
        session :

        file : object
            File object
    """
    filename, body, content_type = file["filename"], file["body"], file["content_type"] 
    uid = uuid4().hex  
    fname = uid + "_" + filename
    uri = ROOT + UPLOAD_FOLDER + fname

    new_source = Source(uid=uid, filename=filename, uri=uri)
    session.add(new_source)
    session.commit()

    with open(UPLOAD_FOLDER + fname, 'wb') as f:
        f.write(body)

    return {
        'URI': ROOT + UPLOAD_FOLDER + fname, 
        'size' : str(len(body) / 1e6) + "MB",
        'filename' : filename,
        'uid' : uid
        }


def get(session, path):
    """Gets file from storage.

    Returns:
        (content_type, binary_data)
    """
    file_location = join(UPLOAD_FOLDER, path)
    if not isfile(file_location):
        raise HTTPError(status_code=404)
    content_type, _ = guess_type(file_location)
    with open(file_location, "rb") as source_file:
        return (content_type, source_file.read())
