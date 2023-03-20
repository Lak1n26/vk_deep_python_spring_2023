import json


def parse_json(
    json_str: str, required_fields: list[str], keywords: list[str], keyword_callback
):
    if required_fields is None or keywords is None:
        return None
    parsed_json = json.loads(json_str)
    return [
        keyword_callback(word)
        for (key, value) in parsed_json.items()
        if key in required_fields
        for word in value.split(" ")
        if word in keywords
    ]
