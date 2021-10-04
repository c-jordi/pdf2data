import os
<<<<<<< HEAD
import copy
from pathlib import Path
from celery import group
from os.path import isfile, join
from mimetypes import guess_type
from urllib import request, parse
from tornado.web import HTTPError
=======
from tornado.web import HTTPError
from os.path import isfile, join
from mimetypes import guess_type
from pathlib import Path
from urllib import request, parse
import copy
>>>>>>> 7540a7982ca3e6d7bd02268a6da1acfc6f192c95

from .models import Source, Project
from . import tasks


<<<<<<< HEAD
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


=======
def extract_features(session, project_id):
    """Extracts the features
    -> Convert the files one by one, and add them to the DB
    table contaning the features
    """

    # We will do first the request to know the specific properties and constants for the
    # feature extraction. Some might be fixed in Constants, but other could depend on specific 
    # inputs from users
    # Essentially, from the Project table we need the level for the extraction of features
    # The 3 levels I have defined so far are: block, textline and page
    all_source = session.query(Source).filter_by(project_id=project_id)
    project_data = session.query(Project).filter_by(id=project_id)
    feature_level = project_data["level"]

    for source in all_source:
        proc_extr_feat(source["uid"], source["xml_uri"], feature_level)



    """
    new_source = Source(uid=uid, filename=filename,
                        pdf_uri=pdf_uri, proc_extractxml_id=proc_extractxml_id)
    session.add(new_source)
    session.commit()        
    """

>>>>>>> 7540a7982ca3e6d7bd02268a6da1acfc6f192c95
def save_features(session, file: object):
    pass
    # TODO: it should look like something as follows, but we need to bear
    # in mind that we are receiving now a dataframe, with many rows, and
    # we need to create one entry in the Feature table per row of the df.
    # Currently, there is only one table for all features. But, at some point
    # we may need to perhaps have 3 tables, for the 3 different levels (block,
<<<<<<< HEAD
    # line and page), as they will have different columns.
=======
    # line and page), as they will have different columns. 
>>>>>>> 7540a7982ca3e6d7bd02268a6da1acfc6f192c95
    """
    new_source = Source(uid=uid, filename=filename,
                        pdf_uri=pdf_uri, proc_extractxml_id=proc_extractxml_id)
    session.add(new_source)
    session.commit()        
    """

<<<<<<< HEAD

=======
>>>>>>> 7540a7982ca3e6d7bd02268a6da1acfc6f192c95
def proc_extr_feat(uid, xml_uri, feature_level):
    """Async extract features after creation of project

    Args:
        xml_uri : (str)
    """
    task = tasks.extract_features.delay(uid, xml_uri, feature_level)
    print("> Worker | Start: feature extraction task:", task.id)
<<<<<<< HEAD
    return task.id
=======
    return task.id
>>>>>>> 7540a7982ca3e6d7bd02268a6da1acfc6f192c95
