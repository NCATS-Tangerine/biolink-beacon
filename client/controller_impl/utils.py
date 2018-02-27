def base_path():
    return 'https://api.monarchinitiative.org/api/'

def biolink_prefix():
    """
    Biolink associations do not generally follow the curie syntax. In such cases
    the resulting statement curie identifier will be set as:

    biolink_prefix() + ':' + biolink_association_id
    """
    return 'biolink'

def get_property(d, key, default_value=None):
    """
    Exhausts each affix before returning default value.

    Parameters
    ----------
    d : dict
        representing a monarch bioentity
    key : str
        the key of the property to be obtained
    """
    affixes = ['_eng', '_std', '_kw']
    try:
        return d[key]
    except:
        for affix in affixes:
            try:
                return d[key + affix]
            except:
                pass
    return default_value

def sanitize_str(s):
    """
    Ensures that s is a string. If it's a list or tuple then it joins the items
    into a string deliminated by a space.
    """
    if isinstance(s, (list, tuple)):
        return ' '.join([sanitize_str(x) for x in s])
    elif isinstance(s, str):
        return s
    else:
        return str(s)

def sanitize_int(i, default_value=1):
    """
    Ensures that i is a positive integer
    """
    return i if isinstance(i, int) and i > 0 else default_value

def try_multi(method, repeats=5, default_value=None, **kwargs):
    """
    Will attempt to call method a number of times, returning the
    results if successful.
    """
    for i in range(repeats):
        try:
            return method(**kwargs)
        except Exception as e:
            pass
    return default_value
