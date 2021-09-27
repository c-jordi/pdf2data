from uuid import uuid4
from .models import Casestudy, Project, Source, Label
from .tasks import process_pdf


def get_all(session):
    """Returns a list of all the projects
    """
    return [project.as_dict() for project in session.query(Project).all()]


def add(session, req):
    """Adds a project to the database.

    Args:
        session :
            Database Session
        req : object
            New project request data
    """
    new_project = create_new_project(req)
    session.add(new_project)
    session.commit()
    new_case = create_new_casestudy(req)
    new_case.project_id = new_project.id
    session.add(new_case)
    new_project.casestudies.append(new_case)
    session.commit()
    sources = load_sources(session, req)
    for source in sources:
        new_project.sources.append(source)
        source.project_id = new_project.id
    labels = add_labels(session, req)
    for label in labels:
        new_case.labels.append(label)
        label.casestudy_id = new_case.id
    session.commit()
    return "ok"


def create_new_project(req):
    """Creates a new project

    Args:
        req : object
    Returns:
        Project
    """
    data = {}
    data["uid"] = uuid4().hex
    data["name"] = req["data"]["project_name"]["value"]
    data["description"] = req["data"]["project_desc"]["value"]
    data["author"] = req["data"]["project_auth"]["value"]
    data["level"] = req["data"]["project_lvl"]["value"]

    return Project(**data)


def create_new_casestudy(req):
    return Casestudy(uid=uuid4().hex)


def add_labels(session, req):
    """Adds labels

    Args: 
        session
        req

    Returns:
        [Label]
    """
    out = []
    labels = req["data"]["project_labels"]["value"]
    for label in labels:
        if label["text"] != "":
            new_label = Label(name=label["text"], color=label["color"])
            session.add(new_label)
            out.append(new_label)
    return out


def load_sources(session, req):
    """Load the project sources

    Args:
        session
        req
    Returns:
        [Source] 
    """
    out = []
    sources = req["data"]["project_src"]["value"]
    for source in sources:
        out.append(session.query(Source).filter_by(uid=source["uid"]).first())
    return out
