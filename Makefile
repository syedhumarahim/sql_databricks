install:
	pip install --upgrade pip && pip install -r requirements.txt

format:	
	black *.py 

lint:
	ruff check *.py helper/*.py 

load_db:
	python -c "from helper.CRUD_functions import load_medical_database; load_medical_database()"

test:
	python -m pytest -vv --cov=. test_main.py --disable-warnings


all: install lint format load_db test

