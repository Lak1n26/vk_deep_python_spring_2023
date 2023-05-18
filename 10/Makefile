all: venv install

venv:
	python -m venv venv
	venv\Scripts\activate && pip install ujson

install:
	venv\Scripts\activate && python setup.py install

test: all
	venv\Scripts\activate && python tests_cjson.py