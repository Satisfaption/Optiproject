def parse_value(value, target_type):
    """parse `value` to `target_type` (int). None if conversion fails"""
    if value in (None, '', 'None'):
        return None
    try:
        if isinstance(value, str) and value.replace('.', '', 1).isdigit():
            value = float(value)
        return target_type(value)
    except (ValueError, TypeError):
        return None