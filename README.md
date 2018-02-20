# Using without Docker (for now)

## Setup

It's recommended that you use a virtual environment, and python 3

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

First we will install some project dependencies

```
(venv) $ pip install tornado==4.5.3 ontobio==0.2.29
```

**Note:** The above ontobio will not work as of yet. You will need to clone git clone -b issue-143 https://github.com/biolink/ontobio.git and install (look at the Dockerfile) for now.

The server and client have been split into two projects, to separate the
Swagger generated code stub, and the implementation details. Because of this
we can safely overwrite the `server` directory and not worry about overwriting
our work.

Install swagger_server

```
(venv) $ cd server
(venv) $ python setup.py install
```

Install controller_impl

```
(venv) $ cd client
(venv) $ python setup.py install
```

## Running

```
(venv) $ cd server
(venv) $ python -m swagger_server
```

Navigate to http://localhost:8080/ui/ in your browser to see the Swagger UI
