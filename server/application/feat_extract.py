import os
import copy
import json
from pathlib import Path
from celery import group
from os.path import isfile, join
from mimetypes import guess_type
from urllib import request, parse
from tornado.web import HTTPError
from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from .models import db, Source, Project
from . import tasks

# ref: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlalchemy/


def save_features(session, uid: str, file: object):
    features = json.loads(file['body'])
    keys = file['keys']
    tablename = "features_" + uid

    FeatureTable = create_table(session, tablename, keys)

    for feature in features:
        save_feature(session, FeatureTable, feature)
    session.commit()


def create_table(session, tablename: str, keys: list):
    attr_dict = {'__tablename__': tablename,
                 'id': Column(Integer, primary_key=True),
                 'bbox': Column(String),
                 'page_id': Column(Integer),
                 'blocktext': Column(String),
                 'pagetext': Column(String)
                 }
    defaults = ['page_id', 'id', 'bbox', 'uid', 'blocktext', 'pagetext']
    attr_dict.update({key: Column(Float)
                     for key in keys if key not in defaults})

    Base = declarative_base()
    FeatureTable = type('FeatureTable', (Base,), attr_dict)
    Base.metadata.create_all(bind=db.engine)
    return FeatureTable


def save_feature(session, FeatureTable, feature: object):
    for key in ["uid", "id"]:
        if key in feature:
            del feature[key]
    row = FeatureTable(**feature)
    session.add(row)
