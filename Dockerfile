FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# COPY requirements.txt /usr/src/app/

# RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN cd ontobio && pip3 install -e .[dev,test] && cd server && python setup.py install && cd .. && cd client && python setup.py install && cd .. && cd server


EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
