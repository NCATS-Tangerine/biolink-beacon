import json

from datetime import date, timedelta

def save(d, file_name):
    """
    Saves d to a file, stamping it with the day.

    Parameters
    ----------
    d : a JSON serializable object, either a dict or list of dicts and lists and primitives.
    file_name : string
    """
    obj = {
        'date' : {
            'year' : date.today().year,
            'month' : date.today().month,
            'day' : date.today().day
        },
        'data' : d
    }

    with open(file_name, 'w') as f:
        json.dump(obj, f)

def load(file_name, max_days_old=3):
    """
    Attempts to load an object saved with save(d, file_name)

    Parameters
    ----------
    file_name : string
    max_days_old :
        the maximum number of days before which the data will not be
        retreived.
    """
    try:
        with open(file_name, 'r') as f:
            obj = json.load(f)
            d = obj['date']
            saved_date = date(d['year'], d['month'], d['day'])

            if date.today() - saved_date > timedelta(days=max_days_old):
                return None
            else:
                return obj['data']

    except FileNotFoundError:
        return None

def base_path():
    # return 'https://api.monarchinitiative.org/api/'
    return 'https://owlsim.monarchinitiative.org/api/'

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
