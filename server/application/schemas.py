from schema import Schema, And, Regex, Or, Literal, Use, Optional, SchemaError

# docs: https://github.com/keleshev/schema

project_req_schema = Schema({
    'name': 'new-project-form',
    'data': {
        'project_name': {
            'value': And(str, lambda x: len(x) > 5),
            Optional(str): Or(str, object)
        },
        'project_desc': {
            'value': str,
            Optional(str): Or(str, object)
        },
        'project_auth': {
            'value': And(str, lambda x: len(x) > 3, Regex(r'^[a-xA-Z\s,]+$')),
            Optional(str): Or(str, object)
        },
        'project_lvl': {
            'value': Or('block', 'page', 'textline'),
            Optional(str): Or(str, object)
        },
        'project_src': {
            'value': And([{
                '_status': str,
                'main_uri': Regex(r'^https?:\/\/[^\s]*$'),
                'filename': str,
                'uid': Regex(r'[0-9a-f]*'),
                Optional(str): str
            }], And(Use(len), lambda x: x > 0)),
            Optional(str): Or(str, object)
        },
        'project_labels': {
            'value': And([{
                'text': str,
                'color': Regex(r'^#[0-9A-F]{3,6}$'),
                'colortext': Regex(r'^#[0-9A-F]{3,6}$'),
                Optional(str): str
            }], And(Use(len), lambda x: x > 0)),
            Optional(str): Or(str, object)
        },
        '_names': list,
        Optional(Regex(r"^__.*")): Or(bool, str),
    }
})

project_upd_schema = Schema({
    'name': 'project-edit-form',
    'data': {
        'project_name': {
            'value': And(str, lambda x: len(x) > 5),
            Optional(str): Or(str, object)
        },
        'project_desc': {
            'value': str,
            Optional(str): Or(str, object)
        },
        'project_auth': {
            'value': And(str, lambda x: len(x) > 3, Regex(r'^[a-xA-Z\s,]+$')),
            Optional(str): Or(str, object)
        },
        '_names': list,
        Optional(Regex(r"^__.*")): Or(bool, str),
    },
    'meta': {
        'uid': str
    }
})
