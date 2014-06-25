test:
	@py.test -s .
	@flake8 .

setup:
	pip install -e .[tests]

.PHONY: test setup
