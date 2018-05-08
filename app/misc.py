from datetime import date

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """自定义JSONEncoder"""
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        try:
            iterator = iter(o)
        except TypeError:
            pass
        else:
            return list(iterator)
        return super().default(o)
