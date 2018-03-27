FROM python:3

RUN mkdir -p /usr/src

COPY /server /usr/src/server
COPY /client /usr/src/client
COPY requirements.txt /usr/src/requirements.txt

# include --no-cache-dir flag when development finalizes?
RUN pip install -r /usr/src/requirements.txt

WORKDIR /usr/src/server
RUN python setup.py install

WORKDIR /usr/src/client
RUN python setup.py install

WORKDIR /usr/src/server

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
