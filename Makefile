venv:
	python -m venv venv
	source venv/bin/activate

download-swagger-ui:
	wget --no-clobber https://files.pythonhosted.org/packages/0e/bb/d00f72e512784af20e368d2ecd5868c51a5aa3688d26ace5f4391651a3ce/swagger_ui_bundle-0.0.3-py3-none-any.whl

installation: download-swagger-ui
	python -m pip install swagger_ui_bundle-0.0.3-py3-none-any.whl
	pip install ontobio
	pip install -r requirements.txt
	pip install connexion[swagger-ui]
	pip install -e client/
	pip install -e server/

.PHONY: server-tests

server-tests:
	cd server && python -m pip install -r test-requirements.txt && nosetests

server-run:
	cd server && python -m swagger_server

api-validation:
	./generate.sh validate

code-generation:
	./generate.sh server

server-build: download-swagger-ui
	docker build -t ncats:biolink .

server-start:
	docker run -d --rm -p 8080:8080 --name biolink ncats:biolink

server-ssh:
	docker exec -it biolink /bin/bash

server-stop:
	docker stop biolink

server-logs:
	docker logs -f biolink
