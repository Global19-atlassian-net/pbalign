SHELL = /bin/bash -e

all: build install

build:
	python setup.py build --executable="/usr/bin/env python"

bdist:
	python setup.py build --executable="/usr/bin/env python"
	python setup.py bdist --formats=egg

install:
	python setup.py install

develop:
	python setup.py develop

pylint:
	pylint --errors-only pbalign

test: pylint
	# Unit tests
	#find tests/unit -name "*.py" | xargs nosetests
	nosetests --verbose tests/unit/*.py
	# End-to-end tests
	@echo pbalign cram tests require blasr installed.
	find tests/cram -name "*.t" | xargs cram 

h5test:
	# Tests for pre-3.0 smrtanalysis when default file formats are *.h5
	@echo pbalign h5 tests require blasr, samtoh5, loadPulses, samFilter and etc installed.
	nosetests --verbose tests/unit_h5/*.py
	find tests/cram_h5 -name "*.t" | xargs cram -v

doc:
	sphinx-apidoc -T -f -o doc pbalign/ && cd doc && make html

docs: doc

doc-clean:
	rm -f doc/*.html

clean: doc-clean
	rm -rf dist/ build/ *.egg-info
	rm -rf doc/_build
	find . -name "*.pyc" | xargs rm -f
	rm -rf dist/
	rm -f nostests.xml

pip-install: 
	@which pip > /dev/null
	@pip freeze|grep 'pbalign=='>/dev/null \
      && ( pip uninstall -y pbalign \
        || pip uninstall -y pbtools.pbalign ) \
      || true
	@pip install --no-index \
          --install-option="--install-scripts=$(PREFIX)/bin" \
          ./

.PHONY: all build bdist install develop test doc clean
