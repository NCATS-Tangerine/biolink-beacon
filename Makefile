venv:
	python -m venv venv
	source venv/bin/activate

install:
	pip install -r requirements.txt
	pip install -e client/
	pip install -e server/
	pip install ontobio

run:
	cd server/
	python -m swagger_server

generate:
	java -jar swagger-codegen-cli.jar generate -i api/knowledge-beacon-api.yaml -l python-flask -o server
