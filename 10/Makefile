all: venv install

venv:
	python -m venv venv
	venv\Scripts\activate && python -m pip install --upgrade pip && pip install -r requirements.txt

install:
	venv\Scripts\activate && python setup.py install

test: all
	venv\Scripts\activate && python tests_cjson.py && python main.py