# biolink-beacon #

Monarch Biolink Knowledge Beacon implementation (as a Python Flask application).

To use this project you must [install flask](http://flask.pocoo.org/docs/0.12/installation/#installation) and [ontobio](http://ontobio.readthedocs.io/en/latest/installation.html). Then in the terminal run the project as described in the [flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/).

On Linux and OSX:

```shell
$ export FLASK_APP=main.py
$ flask run
```

On Windows:

```shell
$ set FLASK_APP=main.py
$ flask run
```

By default it runs at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

Make sure you are using the latest version of python. It is recommended that you install and use this project from within a [virtual environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/).

# issues
- I have made assumptions about how Monarch's semantic categories should be mapped onto the UMLS semantic types that TKBio uses. These assumptions may not be correct, and should be reviewed by the user.
- Many of Monarch's bioentities have multiple semantic categories, but our API requires that the semanticGroup property be a string. For now I have concatenated multiple semantic categories into a single space delimited string.
- For evidence Monarch offers "evidence graphs" which are much like TKBio's concept maps. The monarchinitiative API produces images of these evidence graphs. For now I will just return the same general evidence response for all statements. In the future we may wish to also return images representing the evidence graphs, though.
- At the moment, the ontobio query is filtering on `subject` and `object`, rather than `subject_closure` and `object_closure`. This could be changed to make exact matches automatically added to the query.
- Filtering on semantic groups is not perfect. See issue: https://github.com/biolink/ontobio/issues/52
