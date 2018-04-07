
# Purpose

This repo containes the final code for a live coding talk 
"CI and CD: So Easy You Can Do It Live!" 

During the talk we will:
- create a simple Flask app
- put it on github
- deploy it on heroku.com
- set up continuous integration testing on CircleCI
- set up continuous deployment to heroku
 
# Setup

This project requires Python 3.6 or higher.

Create (free) accounts on:
- GitHub
- CircleCI
- Heroku (and install the Heroku CLI on your machine)


# Let's Do This!

## Create the app

```
mkdir python_talk
cd python_talk
```

We'll install our python packages to a virtual environment
``` 
python3 -m venv env
source env/bin/activate
pip install Flask pytest pylint mypy
pip freeze > requirements.txt
```
Let's add a `Makefile` to create this environment automatically:
```
cat > Makefile
.PHONY: virtualenv setup

virtualenv:
	[ ! -d env ] && python3 -m venv env || true

setup:  virtualenv requirements.txt
	env/bin/pip install -r requirements.txt
	env/bin/pip install -e .
```
We'll need a setup.py so we can do the `pip install -e .`
```
cat > setup.py
import setuptools


setuptools.setup(
    name='talk',
    version='0.0.1',
    long_description='CI / CD demo',
    author='Steve Astels',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
```

Now we can write the app...
```
mkdir src
cat > src/main.py

import flask
import typing
from http import HTTPStatus


App = flask.Flask(__name__)

App.config.update(dict(
    SECRET_KEY='test_key',
))


@App.route('/')
def frontend() -> typing.Tuple[str, int]:
    return 'Woot!', HTTPStatus.OK


if __name__ == "__main__":
    App.run()
```
... and a test
```
mkdir tests
cat > tests/test_main.py

import pytest
from flask import testing
import main
from http import HTTPStatus


@pytest.fixture
def test_client() -> testing.FlaskClient:
    return main.App.test_client()


def test_frontend_route(test_client: testing.FlaskClient) -> None:
    retval = test_client.get('/')
    assert retval.status_code == HTTPStatus.OK
    assert b'Yahoo' in retval.data
```

Let's see if this works!
```
python src/main.py
```
```
pytest
```
Woot!

##  Add code to GitHub

create a new GitHub repo:
- go to https://github.com/
- upper right corner, + / New Repository
- name python_talk
- add Python .gitignore and an MIT License
- Create Repository

Now let's put our project into this repo

```
git init
git add Makefile requirements.txt setup.py src/main.py tests/test_main.py
git commit -m "first commit"
git remote add origin git@github.com:sastels/python_talk.git
git push -u origin master
```

The code should be the GitHub project you created
[https://github.com/sastels/python_talk](https://github.com/sastels/python_talk)


## Run on Heroku

Let's set things up
```
heroku login
pip install gunicorn and add to requirements.txt
pip freeze > requirements.txt
cat > Procfile
web: gunicorn --pythonpath src main:App
```

Put the app on Heroku
```
heroku create
git push heroku master
```

That's it! You can navigate to the web site, or open it with
```
heroku open
```

## Continuous Integration

* go to https://circleci.com/dashboard and add the GitHub project
* cut and paste the `config.yml` file to your project
* run build
* fix `config.yml`:
    * use pytest rather than manage.py,
    * do a pip install -e .


## Continuous Deployment

##### Log in to Heroku from CircleCI

We're going to need our Heroku Login and Heroku API Key.
 
* HEROKU_LOGIN: sastels@gmail.com
* API HEROKU_API_KEY: get at https://dashboard.heroku.com/account

Set these at
[https://circleci.com/gh/sastels/python_talk/edit#env-vars](https://circleci.com/gh/sastels/python_talk/edit#env-vars)

Add this script that CircleCI will use to connect to Heroku.
```
vi .circleci/setup-heroku.sh

#!/bin/bash
git remote add heroku https://git.heroku.com/XXXXXXXXXX.git
wget https://cli-assets.heroku.com/branches/stable/heroku-linux-amd64.tar.gz
sudo mkdir -p /usr/local/lib /usr/local/bin
sudo tar -xvzf heroku-linux-amd64.tar.gz -C /usr/local/lib
sudo ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku

cat > ~/.netrc << EOF
machine api.heroku.com
  login $HEROKU_LOGIN
  password $HEROKU_API_KEY
machine git.heroku.com
  login $HEROKU_LOGIN
  password $HEROKU_API_KEY
EOF
```

##### Make an SSH key for CircleCI

- Make new SSH key
```
ssh-keygen -t rsa -f circleci_key
pbcopy < circleci_key
```

- add to circleci ssh permissions
[https://circleci.com/gh/sastels/python_talk/edit#ssh](https://circleci.com/gh/sastels/python_talk/edit#ssh)

- hostname git.heroku.com
- private key: <paste>
- Make a note of the fingerprint 
(you'll need it in the `config.yml` addition below)

Add the public key to the SSH Keys section of

[https://dashboard.heroku.com/account](https://dashboard.heroku.com/account)

##### Add a deploy section to `config.yml`

Append to config.yml

```
  deploy:
    name: Deploy Master to Heroku
    requires:
      - build
    docker:
      - image: circleci/python:3.6.1
    steps:
      - checkout
      - run: bash .circleci/setup-heroku.sh
      - add_ssh_keys:
          fingerprints:
            - "XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX"
      - run: git push heroku master

workflows:
  version: 2
  build-deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: master
```
