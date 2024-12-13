install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest test_main.py::test_extract

format:	
	black *.py 

lint:
	ruff check *.py mylib/*.py --ignore F401
	
all: install lint test format
