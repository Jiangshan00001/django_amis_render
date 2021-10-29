PYTHON ?= python

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: upload
upload:
	$(PYTHON) -m twine upload dist/*

.PHONY: clean
clean:
	rm  -rf build dist  django_amis_render.egg-info  django_amis_render/__pycache__



.PHONY: test
test:
	pytest

