.PHONY: install reinstall setup test

install:
	pip install . --quiet

reinstall:
	pip uninstall tc_aws -y
	pip install . --quiet

setup:
	@pip install -e .[tests] --quiet

test: setup
	AWS_ACCESS_KEY_ID=test-key pyvows -c -l tc_aws
