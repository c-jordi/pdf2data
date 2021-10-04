import os
from uuid import uuid4
import time
import subprocess
import tempfile
import json
from urllib import request, parse
from pathlib import Path
from celery import Celery
from celery.result import AsyncResult

import xmltodict

from . import storage
import xml.etree.ElementTree as ET

from .utils_files import extract_xml, clean_xml, get_text_onefile, \
    convert_textlines_in_xml_tree, create_tmp, \
    info_from_uri

from application.features import feature_parsing
from .constants import API_AUTH, TMP_FOLDER, ROOT, UPLOAD_FOLDER


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
    print("UID:", uid, "URI", uri)
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
    xml_uri_tmp = create_tmp(name + '.xml')
    xml_tree.write(xml_uri_tmp, encoding='utf-8')
    # 6. Reading the str from the xml file
    with open(xml_uri_tmp, 'r') as f:
        all_text = f.readlines()
    xml_dict = xmltodict.parse('\n'.join(all_text))
    # 7. Removing all tmp created
    os.remove(uri_out)
    os.remove(xml_uri_tmp)

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

    # Replace with the uri contained in the server response
    xml_uri = uri.replace(".pdf", ".xml")

    return uid, xml_uri


@celery.task(name="extract_features")
def extract_features(xml_info, parser_type):
    """
    This task is trigerred once the project is created, i.e., when we
    know the level of the features. Besides, it is triggered again when
    some changes are done on the features menu, or when new files are added
    """

    # Get the file
    [uid, xml_uri] = xml_info
    _, name, suffix = info_from_uri(xml_uri)

    # Now, we call the function that parse the document and obtain the features
    parser_name = "textblock_type"
    if parser_type == "textline":
        parser_name = "textline_type"
    elif parser_type == "page":
        parser_name = "page_type"
    doc_parser = feature_parsing.get_available_parsers()[parser_name]
    features_file = feature_parsing.extract_features_for_file(
        doc_parser, xml_uri)

    # The dataframe is returned, and then, we send it back to the server, that will
    # store it in the DBs
    print(features_file.to_json(orient="records"))
    return
    return features_file

    # TODO: here we are just sending for the moment the dataframe, as I was testing this
    # but this function needs to call the handler tasks/save_features, send the dataframe,
    # and this will store this in the DB table Features

    """
    dict_data = {"status": "processed", "uid": uid, "data":
                 {"filename": name, "body": features_file, "content_type": "pandas"}}
    data = json.dumps(dict_data).encode("utf-8")
    req = request.Request(
        "http://localhost:8888/tasks/save_features", data=data)
    req.add_header("Token", API_AUTH)
    request.urlopen(req)
    # Sending the request
    return {"status": True}
    """
