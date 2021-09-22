from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.expression import desc, true
from sqlalchemy.sql.sqltypes import Boolean
from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    name = Column(String)
    description = Column(String, nullable=False)
    author = Column(String, nullable=False)
    level = Column(String, nullable=False)
    sources = relationship("Source")
    casestudies = relationship("Casestudy")

    def __init__(self, name=None, uid="", description="No description", author="No author", level="page", sources=[]):
        self.name = name
        self.uid = uid
        self.description = description
        self.author = author
        self.level = level
        self.sources = sources

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["sources"] = [source.as_dict() for source in self.sources]
        data["labels"] = [label.as_dict()
                          for case in self.casestudies for label in case.labels]
        return data


class Casestudy(db.Model):
    __tablename__ = "casestudies"
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    author = Column(String)
    notes = Column(Text)
    vocab_flag = Column(String)
    n_words_use_features = Column(String)
    classifier_type = Column(String)
    freq_matrix_type = Column(String)
    n_estimators_classif = Column(String)
    training_type = Column(String, default="Train")
    retrain_interval = Column(Integer)
    name_table_samples_inf = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    labels = relationship("Label")

    def __init__(self, uid, name="", description="", author=""):
        self.uid = uid
        self.name = name
        self.description = description
        self.author = author


class Label(db.Model):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String(7), nullable=False)
    casestudy_id = Column(Integer, ForeignKey('casestudies.id'))

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return "[Label: {} | {}]".format(self.name, self.color)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

"""
File naming convention:
uid: unique id generated with uuid4().hex
filename: original name of the file, and for newly created files, simplified 
    name in case the file needs to be exported
uri: the localhost location of the file + uid + _ + filename
"""

class Source(db.Model):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    filename = Column(String, nullable=False)
    uri = Column(String, nullable=False, unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    preproc_id = Column(String)
    preproc_ok = Column(Integer, default=0)

    def __init__(self, uid, filename, uri, project_id=None, preproc_id=None):
        self.uid = uid
        self.filename = filename
        self.uri = uri
        self.project_id = None
        self.preproc_id = preproc_id

    def __repr__(self):
        return f"<Source: {self.filename}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Page(db.Model):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    source_id = Column(Integer, ForeignKey('sources.id'))
    page_number = Column(Integer, nullable=False)
    annotated = Column(Boolean, default=False)


class Annotation(db.Model):
    __tablename__ = 'annotations'
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    casestudy_id = Column(Integer, ForeignKey('casestudies.id'))
    page_id = Column(Integer, ForeignKey('pages.id'))
    bbox = Column(String)
    time_labelling = Column(String)
    split = Column(String)


if __name__ == "__main__":
    db.configure(url='sqlite:///db.sqlite')
    db.create_all()
