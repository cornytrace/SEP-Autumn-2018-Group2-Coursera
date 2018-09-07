# SEP Autumn 2018 Group 2 EIT-Dashboard

[![Build Status](https://travis-ci.com/cornytrace/SEP-Autumn-2018-Group2-Backend.svg?token=ksRe83PxhypHvSJboCmE&branch=master)](https://travis-ci.com/cornytrace/SEP-Autumn-2018-Group2-Backend)

## Installation

### Preparation

Install Python 3.6: https://www.python.org

If you use Visual Studio Code, install the Python extension and add the following to your preferences:

``` json
"python.linting.pylintEnabled": false,
"python.formatting.provider": "black",
"[python]": {
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
},
```  

This will ensure that your code is automatically fixed to conform to our coding style.

If you use another editor, follow their instructions to enable black and isort, and to enable fix-on-save.

### Install pipenv

``` bash
$ pip3 install pipenv

```

### Clone repo

``` bash
# clone the repo
$ git clone https://github.com/cornytrace/SEP-Autumn-2018-Group2-Backend eit-dash-backend

# go into app's directory
$ cd eit-dash-backend

```

## Backend

``` bash

# install app's dependencies
$ pipenv sync --dev

# create database
$ pipenv run python manage.py migrate
```

### Usage

``` bash
# run the site with hot reload at localhost:8000
$ pipenv run python manage.py runserver

# run linter
$ pipenv run black .

# run isort
$ pipenv run isort . -rc

# run unit tests with coverage
$ pipenv run pytest --cov

# generate full coverage report in htmlcov/
$ pipenv run coverage html

```

## Documentation

[Django](https://docs.djangoproject.com/en/2.1/)

[pytest](https://docs.pytest.org/en/latest/contents.html)

[pytest-django](https://pytest-django.readthedocs.io/en/latest/)
