from uuid import uuid4
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type
from pathlib import Path
from urllib import request, parse
import xml.etree.ElementTree as ET

import pickle as pkl

import xmltodict

from .models import Source
from .constants import ROOT, UPLOAD_FOLDER, SEP_UID_NAME
from . import tasks


def upload(session, file: object):
    """Uploads file to storage.

    Args:
        session
        file 

    Returns:
        object
    """
    filename, body, content_type = file["filename"], file["body"], file["content_type"]
    if content_type == "zip":
        return upload_zip(session, file)

    if content_type != "application/pdf":
        return {
            'status': "Wrong file type."
        }
    return upload_pdf(session, file)


def upload_zip(session, file):
    """Uploads zip
    """
    pass


def upload_pdf(session, file):
    """Uploads pdf
    """
    uid = uuid4().hex
    filename, body, content_type = file["filename"], file["body"], file["content_type"]
    fname = uid + SEP_UID_NAME + Path(filename).stem + Path(filename).suffix
    pdf_uri = ROOT + UPLOAD_FOLDER + fname

    with open("application/" + UPLOAD_FOLDER + fname, 'wb') as f:
        f.write(body)

    # proc_extractxml_id = proc_extractxml(uid, pdf_uri)  # Begin the extraction of the xml

    new_source = Source(uid=uid, filename=filename,
                        main_uri=pdf_uri)

    session.add(new_source)
    session.commit()

    return {
        'main_uri': pdf_uri,
        'size': str(round(len(body) / 1e6, 2)) + "MB",
        'filename': filename,
        'uid': uid
    }


def add_xml(session, uid: str, file: object):
    """Adds any file to storage, assigning a uid, saving it and adding to source table

    Args:
        session :
        uid : source unique identifier
        file : file object
    """
    filename, body, content_type = file["filename"], file["body"], file["content_type"]
    name = Path(filename).stem + Path(filename).suffix
    fname = uid + SEP_UID_NAME + name
    xml_uri = ROOT + UPLOAD_FOLDER + fname

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
    print("> Storage | Save: XML file")
    print("Saved at:", name_out)

    update(session, uid, {
        "xml_uri": xml_uri,
        "proc_extractxml_status": "done"
    })

def add_pkl(session, uid: str, file: object):
    """Creates pickle from content passed, assigning a uid, saving it and adding to source table

    Args:
        session :
        uid : source unique identifier
        file : file object
    """
    filename, content_body, content_type = file["filename"], file["body"], file["content_type"]
    name = Path(filename).stem + Path(filename).suffix
    fname = uid + SEP_UID_NAME + name
    pkl_uri = ROOT + UPLOAD_FOLDER + fname

    # The saving of an xml tree is slightly different
    name_out = "application/" + UPLOAD_FOLDER + fname
    if content_type == "pkl":
        pkl.dump(content_body, open(name_out, 'wb'))
        print("> Storage | Save: PKL file")
        print("Saved at:", name_out)

        new_source = Source(uid=uid, filename=filename,
                            main_uri=pkl_uri)
        session.add(new_source)
        session.commit()        
    else:
        print("Mismatch! Not PKL, but rather {}".format(content_type))

def update(session, uid, data):
    """Update source file.

    Args:
        session 
        uid : (str) unique identifier of the source file
        data : (object)
    """
    source = session.query(Source).filter_by(uid=uid)
    source.update(data)
    session.commit()


def get(path):
    """Gets file from storage.

    Returns:
        (content_type, binary_data)
    """
    file_location = join("application/"+UPLOAD_FOLDER, path)
    print("file location:", file_location)
    if not isfile(file_location):
        raise HTTPError(status_code=404)
    content_type, _ = guess_type(file_location)
    with open(file_location, "rb") as source_file:
        return (content_type, source_file.read())
