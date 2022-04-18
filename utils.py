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

class KNBError(Exception):
    pass

class Choices:
    STONE = 0
    PAPER = 1
    SCISSORS = 2
    ALL = STONE, PAPER, SCISSORS

    @staticmethod
    def who_wins(choice1, choice2):
        if choice1 == choice2:
            return 0
        if choice1 == Choices.STONE and choice2 == Choices.SCISSORS:
            return 1
        if choice2 == Choices.STONE and choice1 == Choices.SCISSORS:
            return 2
        return 1 if choice1 > choice2 else 2