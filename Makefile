TEMPFILE := $(shell mktemp -u)

.PHONY: install clean uninstall venv doc docs html api

install:
	sh ./bump-version.sh
	pip3 install -r requirements.txt
	python3 setup.py install

uninstall:
	python3 setup.py install --record ${TEMPFILE} && \
	cat ${TEMPFILE} | xargs rm -rf && \
	rm -f ${TEMPFILE}

devenv:
	@echo "Installing latest development requirements"
	pip3 install -U --force-reinstall -r dev_requirements.txt

check:
	@# set timeout so we do not wait in infinite loops and such
	@# Make sure we have -p no:celery otherwise py.test is trying to do dirty stuff with loading celery.contrib
	PYTHONPATH="test/:${PYTHONPATH}" python3 -m pytest -s -vvl --timeout=2 --nocapturelog -p no:celery test/
	@[ -n "${NOPYLINT}" ] || { echo ">>> Running PyLint"; pylint selinonlib; }
	#@[ -n "${NOCOALA}" ] || { echo ">>> Running Coala bears"; coala --non-interactive; }
	@[ -n "${NOPYDOCSTYLE}" ] || { echo ">>> Running pydocstyle"; find selinonlib/ -name '*.py' -and ! -name 'test_*.py' -and ! -name 'codename.py' -and ! -name 'version.py' ! -path 'selinonlib/predicates/*' -print0 | xargs -0 pydocstyle {} \; ; }

devenv:
	@echo "Installing latest development requirements"
	pip3 install -U -r dev_requirements.txt

venv:
	virtualenv venv && source venv/bin/activate && pip3 install -r requirements.txt
	@echo "Run 'source venv/bin/activate' to enter virtual environment and 'deactivate' to return from it"

clean:
	find . -name '*.pyc' -or -name '__pycache__' -print0 | xargs -0 rm -rf
	rm -rf venv docs/ build dist selinonlib.egg-info

api:
	@sphinx-apidoc -e -f -o docs.source/selinonlib/doc selinonlib -f

doc:
	@make -f Makefile.docs html
	@echo "Documentation available at 'docs/index.html'"

docs: doc
html: doc
test: check

