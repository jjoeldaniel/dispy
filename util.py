import json


def load_filter(d: str):
    d = json.loads(d)
    return {(k, v) for (k, v) in d.items() if v}
