import os
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type
from pathlib import Path
from urllib import request, parse
import copy

from .models import Source, Project
from . import tasks


def extract_features(session, project_id):
    """Extracts the features
    -> Convert the files one by one, and add them to the DB
    table contaning the features
    """

    # We will do first the request to know the specific properties and constants for the
    # feature extraction. Some might be fixed in Constants, but other could depend on specific 
    # inputs from users
    all_source = session.query(Source).filter_by(project_id=project_id)
    project_data = session.query(Project).filter_by(id=project_id)
    feature_level = project_data["level"]

    for source in all_source:
        proc_extr_feat(source["uid"], source["xml_uri"])

    """
    new_source = Source(uid=uid, filename=filename,
                        pdf_uri=pdf_uri, proc_extractxml_id=proc_extractxml_id)
    session.add(new_source)
    session.commit()        
    """

def save_features(session, file: object):

    new_source = Source(uid=uid, filename=filename,
                        pdf_uri=pdf_uri, proc_extractxml_id=proc_extractxml_id)
    session.add(new_source)
    session.commit()        

def proc_extr_feat(uid, xml_uri):
    """Async preprocess pdf after upload.

    Args:
        uri : (str)
    """
    task = tasks.extract_features.delay(uid, xml_uri)
    print("> Worker | Start: feature extraction task:", task.id)
    return task.id