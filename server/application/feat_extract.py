import os
import copy
from pathlib import Path
from celery import group
from os.path import isfile, join
from mimetypes import guess_type
from urllib import request, parse
from tornado.web import HTTPError

from .models import Source, Project
from . import tasks


def apply(project):
    """Runs the conversion of pdfs to xmls and the feature extraction asynchronously. 

    Args:
        project
    """
    feature_level = project.level
    header = [tasks.process_pdf.s(s.uid, s.pdf_uri) | tasks.extract_features.s(feature_level)
              for s in project.sources]
    task = group(header).delay()

    return task.id


def save_features(session, file: object):
    pass
    # TODO: it should look like something as follows, but we need to bear
    # in mind that we are receiving now a dataframe, with many rows, and
    # we need to create one entry in the Feature table per row of the df.
    # Currently, there is only one table for all features. But, at some point
    # we may need to perhaps have 3 tables, for the 3 different levels (block,
    # line and page), as they will have different columns.
    """
    new_source = Source(uid=uid, filename=filename,
                        pdf_uri=pdf_uri, proc_extractxml_id=proc_extractxml_id)
    session.add(new_source)
    session.commit()        
    """


def proc_extr_feat(uid, xml_uri, feature_level):
    """Async extract features after creation of project

    Args:
        xml_uri : (str)
    """
    task = tasks.extract_features.delay(uid, xml_uri, feature_level)
    print("> Worker | Start: feature extraction task:", task.id)
    return task.id
