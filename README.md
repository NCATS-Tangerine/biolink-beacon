# Using without Docker (for now)

## Setup

It's recommended that you use a virtual environment, and python 3

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

First we will install some project dependencies

```
(venv) $ pip install tornado==4.5.3
```

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
(venv) $ cd backend
(venv) $ python setup.py install
```

## Running

```
(venv) $ cd server
(venv) $ python -m swagger_server
```

Navigate to http://localhost:8080/ui/ in your browser to see the Swagger UI
