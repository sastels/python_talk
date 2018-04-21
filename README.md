
# Purpose

This repo contains the final code for a live coding talk 
"CI / CD for the Masses" 

During the talk we will:
- create a simple Flask app
- put it on GitHub
- deploy it on Heroku
- set up continuous integration testing on CircleCI
- set up continuous deployment to Heroku
 
# Setup

This project requires Python 3.6 or higher, as well as `pipenv`.

Create (free) accounts on:
- GitHub
- CircleCI
- Heroku (and install the Heroku CLI on your machine)


# Let's Do This!

## Make a repo in GitHub

Create a new GitHub repo:
- go to GitHub
- upper right corner, + / New Repository
- name ci_cd_demo
- add Python .gitignore and an MIT License
- Create Repository

Clone locally:
```
git clone git@github.com:sastels/ci_cd_demo.git
cd ci_cd_demo
```


## Create the app

We'll install our python packages to a virtual environment using `pipenv`
```
pipenv install Flask pytest
```

Now we can write the app. First `main.py`:
```
import flask
from http import HTTPStatus


App = flask.Flask(__name__)

App.config.update(dict(
    SECRET_KEY='test_key',
))


@App.route('/')
def frontend():
    return 'Woot!', HTTPStatus.OK


if __name__ == "__main__":
    App.run()
```

Next `test_main.py`
```
import pytest
from flask import testing
import main
from http import HTTPStatus


@pytest.fixture
def test_client():
    return main.App.test_client()


def test_frontend_route(test_client):
    retval = test_client.get('/')
    assert retval.status_code == HTTPStatus.OK
    assert b'Yahoo' in retval.data
```

Let's see if this works!
```
python main.py
```
```
pytest
```
Test fails - fix and it passes. Woot!

##  Add code to GitHub

```
git status
```
Have some cruft: `.pytest_cache/`, maybe `test_main.py~`. Append to .gitignore:
```
*~
.pytest_cache
```

Now let's put our project into this repo

```
git add .
git commit -m "flask app"
git push
```

The code should be the GitHub project you created
[https://github.com/sastels/ci_cd_demo](https://github.com/sastels/ci_cd_demo)


## Run on Heroku

We will use the `gunicorn` web server.
```
pipenv install gunicorn
```
We use `Procfile` to tell Heroku how to run the app: 
```
web: gunicorn main:App
```

Update the repo
```
git add .
git commit -m "Heroku setup"
git push
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
    * use `pytest` rather than `python manage.py test`,


## Continuous Deployment

##### Log in to Heroku from CircleCI

We're going to need our Heroku Login and Heroku API Key.
 
* HEROKU_LOGIN: sastels.demo@gmail.com
* HEROKU_API_KEY: get at https://dashboard.heroku.com/account

Set these at
[https://circleci.com/gh/sastels/ci_cd_demo/edit#env-vars](https://circleci.com/gh/sastels/ci_cd_demo/edit#env-vars)

Add this script `.circleci/setup-heroku.sh` that CircleCI will use to connect to Heroku.
```
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
