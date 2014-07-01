test:
	@py.test -s .
	@flake8 --max-line-length=110 .

setup:
	pip install -e .[tests]

.PHONY: test setup
