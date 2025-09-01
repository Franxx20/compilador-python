from constantes import MAX_STRING_LENGHT

class invalid_lenght_exception(Exception):
    pass

def validate_float(value):
    try:
        f = float(value)
        if f.is_infinite() or f.is_nan():
            return False
        return True
    except ValueError:
        return False

def validate_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_string(value, max_length=MAX_STRING_LENGHT):
    if isinstance(value, str) and len(value) <= max_length:
        return True
    return False