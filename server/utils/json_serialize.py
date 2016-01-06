import json
from bson import ObjectId
from functools import partial

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
           return str(o)
        return json.JSONEncoder.default(o)

dumps = partial(json.dumps, cls=JSONEncoder)
