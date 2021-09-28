from fuzzywuzzy import fuzz

from . import projects

MATCH_CUTOFF = 85


def run(session, data):
    """Query data
    """
    query = data["query"]
    _projects = projects.get_all(session)
    _scored_projects = list(map(lambda x: score_name(query, x), _projects))
    _filtered_projects = list(
        filter(lambda x: x["_score"] >= 85, _scored_projects))
    _formatted_projects = list(map(format_project, _filtered_projects))
    return _formatted_projects


def score_name(string: str, el: object):
    score_1 = fuzz.partial_ratio(el["name"].lower(), string.lower())
    score_2 = fuzz.ratio(el["name"].lower(), string.lower())
    score_3 = fuzz.token_sort_ratio(el["name"].lower(), string.lower())
    el["_score"] = max(score_1, score_2, score_3)
    return el


def format_project(el):
    return {
        "label": el["name"],
        "url": "/annotate/" + el["uid"],
        "settings": "/project/" + el["uid"],
    }
