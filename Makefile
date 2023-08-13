all:
	@echo "make docs - Generates documentation for the project and serves it on http://localhost:1234"
	@echo "make run - Runs the process to read all files and coerce them into a SQLite database"
	@echo "make test - Runs unit tests"

docs:
	python -m pydoc -p 1234

run:
	python src/process.py

test:
	python -m unittest discover -s tests -p 'test_*.py' -q