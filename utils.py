from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

__paths = {}

def get_path(path):
    return __paths.get(path)

def validate_json(args, schema=None):
    if len(args) == 1 or schema is None:
        return True
    try:
        validate(instance=args[1], schema=schema)
    except ValidationError:
        return False
    else:
        return True

def pathhandler(path, schema=None):
    def outerWrapper(func):
        if path in __paths:
            raise ImportError(f'path {path} already exists')
        __paths[path] = func
        def innerWrapper(*args, **kwargs):
            if validate_json(args, schema):
                return func(*args, **kwargs)
        return innerWrapper
    return outerWrapper

