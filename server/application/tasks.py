import os
from uuid import uuid4
import time
import subprocess
import tempfile
import json
from urllib import request, parse
from pathlib import Path
from celery import Celery

import xmltodict

from . import storage
import xml.etree.ElementTree as ET

from .utils_files import extract_xml, clean_xml, get_text_onefile, \
    convert_textlines_in_xml_tree, create_tmp, \
    info_from_uri
from .constants import API_AUTH, TMP_FOLDER


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "pyamqp://guest@localhost//")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")


@celery.task(name="process_pdf")
def process_pdf(uid, uri):
    """Process file after upload.

    Args:
        uid : (str)
        uri : (str)

    Returns:
        (object) : Status info
    """
    # Get the file
    uid, name, suffix = info_from_uri(uri)

    # We need to preload the file into a file, and then read from it to make
    # it seekable
    # https://stackoverflow.com/questions/58702442/wrap-an-io-bufferediobase-such-that-it-becomes-seek-able

    # Processing steps
    # 1. Extracting and saving the original xml
    uri_out = extract_xml(uri)
    # 2. Opening the xml, and cleaning the properties of text
    root_xml = clean_xml(uri_out)
    # 3. Removing the text level from the hierarchy
    root_xml = get_text_onefile(root_xml)
    # 4. Add an extra level on the xml hierarchy grouping things
    # font characteristics
    root_xml = convert_textlines_in_xml_tree(root_xml)
    xml_tree = ET.ElementTree(root_xml)
    # 5. Saving tmp xml into file, to open it again as str, and then
    # allow it serialization
    uri_xml = create_tmp(name + '.xml')
    xml_tree.write(uri_xml, encoding='utf-8')
    # 6. Reading the str from the xml file
    with open(uri_xml, 'r') as f:
        all_text = f.readlines()
    xml_dict = xmltodict.parse('\n'.join(all_text))
    # 7. Removing all tmp created
    os.remove(uri_out)
    os.remove(uri_xml)

    # Once obtained all the information from the pdf, we need to contact the handlers to
    # stored the generated files, and add the files to the source table in the DB

    # Send the processed file
    # The pdf is added on the main one
    dict_data = {"status": "processed", "uid": uid, "data":
                 {"filename": name + '.xml', "body": xml_dict, "content_type": "xml"}}
    data = json.dumps(dict_data).encode("utf-8")
    req = request.Request("http://localhost:8888/tasks/save_xml", data=data)
    req.add_header("Token", API_AUTH)
    request.urlopen(req)
    # Sending the request
    return {"status": True}
