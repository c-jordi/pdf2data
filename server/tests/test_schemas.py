from application.schemas import *
from copy import deepcopy
import pytest

valid_req = {
    'name': 'new-project-form',
    'data': {
        'project_name': {'value': 'New test title'},
        'project_desc': {'value': 'Test desc'},
        'project_auth': {'value': 'Test author, Another Test'},
        'project_lvl': {'value': 'block'},
        'project_src': {'value': [{'_status': 'uploaded', 'URI': 'http://test_url', 'filename': 'No_Service.mp3', 'uid': '459a7eb3'}],
                        'project_labels': {'value': [{'text': 'Label a', 'color': '#3E7BE2', 'colortext': '#3E7BE2'}],
                                           '__valid': True}
                        },
        'project_labels': {
            'value': [
                {"color": "#123AAA", "colortext": "#122",
                    'text': "Some simple label"}
            ]
        },
        "_names": []
    }
}


def test_valid_project_req():
    assert(project_req_schema.validate(valid_req))


def raises_schema_error(req):
    with pytest.raises(SchemaError):
        project_req_schema.validate(req)


def test_invalid_project_header():
    invalid_req = deepcopy(valid_req)
    invalid_req['name'] = 'different name'
    raises_schema_error(invalid_req)


def test_invalid_project_name():
    invalid_req = deepcopy(valid_req)
    invalid_req['data']['project_name'] = 'inva'
    raises_schema_error(invalid_req)
