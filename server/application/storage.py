import re, os
from uuid import uuid4
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type
from pathlib import Path
from urllib import request, parse
import xml.etree.ElementTree as ET

import xmltodict

from .models import Source
from .constants import ROOT, UPLOAD_FOLDER, SEP_UID_NAME
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
    fname = uid + SEP_UID_NAME + Path(filename).stem + Path(filename).suffix
    uri = ROOT + UPLOAD_FOLDER + fname

    # First add the pdf file to the storage folder, as we need it for the preprocessing
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

def add_anyfile(session, file):
    """Adds any file to storage, assigning a uid, saving it and adding to source table

    Args:
        session :
        file : object
            File object
    """
    filename, body, content_type = file["filename"], file["body"], file["content_type"]
    uid = uuid4().hex
    name = Path(filename).stem + Path(filename).suffix
    fname = uid + SEP_UID_NAME + name
    uri = ROOT + UPLOAD_FOLDER + fname

    # The saving of an xml tree is slightly different
    name_out = "application/" + UPLOAD_FOLDER + fname
    if content_type == "xml":
        xml_text = xmltodict.unparse(body, pretty=True)
        root_xml = ET.fromstring(xml_text)
        xml_tree = ET.ElementTree(root_xml)
        xml_tree.write(name_out, encoding="utf-8")
    else:
        with open(name_out, 'wb') as f:
            f.write(body)

    # TODO
    print("TODO: don't undestand so far the use of this ID")
    preproc_id = "dummy_id"
    new_source = Source(uid=uid, filename=name,
                        uri=uri, preproc_id=preproc_id)
    session.add(new_source)
    session.commit()

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
