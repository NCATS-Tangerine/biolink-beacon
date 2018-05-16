FROM python:3

RUN mkdir -p /usr/src

COPY /server /usr/src/server
COPY /client /usr/src/client
COPY requirements.txt /usr/src/requirements.txt

# include --no-cache-dir flag when development finalizes?
RUN pip install --upgrade pip && \
    pip install -r /usr/src/requirements.txt && \
    pip install /usr/src/server/ && \
    pip install /usr/src/client/ && \
    pip install ontobio

WORKDIR /usr/src/server

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
