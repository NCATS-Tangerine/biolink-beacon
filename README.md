# biolink-beacon #

Monarch Biolink Knowledge Beacon implementation (as a Python Flask application).

## Quickstart (Using Docker) ##

This project is designed to run as a Docker container. Note that although the Docker client used to manage containers runs on several operating systems, the container engine currently only runs under Linux. See the [Docker Guide] (https://docs.docker.com/get-started/) for details on how to install Docker.

Then with Docker installed, you can build an image from the `Dockerfile` provided in the main directory of this project.

```shell
cd biolink-beacon
docker build -t ncats:biolink .
```

Note that depending on your Docker installation, you may need to run the docker command as 'sudo'.  Within the Docker container, the Flask app is set to run at `0.0.0.0:5000`. You can re-map ports when you run a Docker image with the `-p` flag.

```shell
docker run --rm -p 8080:5000 ncats:biolink
```

Now open your browser to `localhost:8080` to see the application running.

## Running the Server Outside Docker ##

You must [install flask](http://flask.pocoo.org/docs/0.12/installation/#installation) and [ontobio](http://ontobio.readthedocs.io/en/latest/installation.html). Then in the terminal run the project as described in the [flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/).

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

By default it runs at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). You can change the host and port with `-h` and `-p` flags as such:

```shell
$ flask run -h 0.0.0.0 -p 8080
```

Make sure you are using the latest version of python. It is recommended that you install and use this project from within a [virtual environment](https://virtualenv.pypa.io/en/latest/).

## Issues ##
- I have made assumptions about how Monarch's semantic categories should be mapped onto the UMLS semantic types that TKBio uses. These assumptions may not be correct, and should be reviewed by the user.
- Many of Monarch's bioentities have multiple semantic categories, but our API requires that the semanticGroup property be a string. For now I have concatenated multiple semantic categories into a single space delimited string.
- For evidence Monarch offers "evidence graphs" which are much like TKBio's concept maps. The monarchinitiative API produces images of these evidence graphs. For now I will just return the same general evidence response for all statements. In the future we may wish to also return images representing the evidence graphs, though.
- Filtering on semantic groups is not perfect. See issue: https://github.com/biolink/ontobio/issues/52
- The /types query doesn't reflect all the data there is. See issue: https://github.com/biolink/ontobio/issues/78
