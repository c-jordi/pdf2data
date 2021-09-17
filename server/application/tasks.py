import os
import time
import subprocess
import tempfile
import json
from urllib import request, parse
from pathlib import Path
from celery import Celery

from .constants import API_AUTH


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
    name = Path(uri).name
    suffix = Path(uri).suffix
    resp = request.urlopen(uri)

    # Do some processing
    with tempfile.TemporaryFile() as temp:
        temp.write(resp.read())

    # Send the processed file
    data = json.dumps({"status": "processed", "uid": uid}).encode("utf-8")
    req = request.Request("http://localhost:8888/tasks/preproc", data=data)
    req.add_header("Token", API_AUTH)
    request.urlopen(req)

    return {"status": True}
