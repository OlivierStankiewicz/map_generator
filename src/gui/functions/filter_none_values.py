def filter_none_values(obj):
    """Recursively remove keys with None values from dictionaries or lists."""
    if isinstance(obj, dict):
        return {k: filter_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [filter_none_values(item) for item in obj if item is not None]
    else:
        return obj