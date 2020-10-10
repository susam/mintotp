URI1 = otpauth://totp/alice:bob?secret=ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS
URI2 = otpauth://totp/alice:cam?secret=PW4YAYYZVDE5RK2AOLKUATNZIKAFQLZO&issuer=alice

help:
	@echo 'Release Checklist'
	@echo '================='
	@echo
	@echo 'vim setup.py    # Update version'
	@echo 'vim CHANGES.md  # Update changelog'
	@echo
	@echo 'make checks'
	@echo 'make dist test-upload verify-test-upload'
	@echo 'open https://test.pypi.org/project/mintotp/'
	@echo
	@echo 'git add .'
	@echo 'git status'
	@echo 'git commit'
	@echo 'git push origin master'
	@echo
	@echo 'make upload verify-upload'
	@echo 'open https://pypi.org/project/mintotp/'
	@echo
	@echo "VER=$$(grep version setup.py | cut -d\' -f2)"
	@echo 'git tag $$VER -m "MinTOTP $$VER"'
	@echo 'git push origin $$VER'
	@echo

# Development.
rmvenv:
	rm -rf ~/.venv/mintotp venv

venv: FORCE
	python3 -m venv ~/.venv/mintotp
	echo . ~/.venv/mintotp/bin/activate > venv

deps:
	touch venv
	. ./venv && \
	    pip3 install pylama pylama-pylint coverage wheel twine coveralls

test:
	python3 -m unittest -v

coverage:
	. ./venv && coverage run -m unittest -v
	. ./venv && coverage report --show-missing
	. ./venv && coverage html

lint:
	. ./venv && isort --quiet --diff .
	. ./venv && pylama \
	    -l pycodestyle,pyflakes,mccabe,pylint,isort \
	    -i C0111,C0103,R0201

checks: lint test coverage dist


# Helpers.
qr:
	qrencode -s 10 -o secret1.png "$(URI1)"
	qrencode -s 10 -o secret2.png "$(URI2)"

key:
	python3 -c \
	'import base64, os; print(base64.b32encode(os.urandom(20)).decode())'


# Package and distribute.
dist: clean venv
	. ./venv && python3 setup.py sdist bdist_wheel
	. ./venv && twine check dist/*
	unzip -c dist/*.whl */METADATA

upload:
	. ./venv && twine upload dist/*

test-upload:
	. ./venv && twine upload --repository-url \
	    https://test.pypi.org/legacy/ dist/*


# Test distributions.
user-venv: FORCE
	rm -rf ~/.venv/test-mintotp user-venv
	python3 -m venv ~/.venv/test-mintotp
	echo . ~/.venv/test-mintotp/bin/activate > user-venv

verify-upload:
	$(MAKE) verify-sdist
	$(MAKE) verify-bdist

verify-test-upload:
	$(MAKE) verify-test-sdist
	$(MAKE) verify-test-bdist

verify-sdist: user-venv
	. ./user-venv && pip3 install --no-binary :all: mintotp
	. ./user-venv && echo ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | mintotp

verify-bdist: user-venv
	. ./user-venv && pip3 install mintotp
	. ./user-venv && echo ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | mintotp

verify-test-sdist: user-venv
	. ./user-venv && pip3 install \
	    --index-url https://test.pypi.org/simple/ --no-binary :all: mintotp
	. ./user-venv && echo ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | mintotp

verify-test-bdist: user-venv
	. ./user-venv && pip3 install \
	    --index-url https://test.pypi.org/simple/ mintotp
	. ./user-venv && echo ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS | mintotp

clean:
	rm -rf *.pyc __pycache__
	rm -rf .coverage htmlcov
	rm -rf build dist mintotp.egg-info

FORCE:
