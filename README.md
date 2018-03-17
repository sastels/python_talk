
Assumption: have accounts on
- github
- circleci
- heroku



-- Setup --

mkdir Python_Talk
cd Python_Talk

virtualenv venv
pip install Flask pytest pylint mypy

pip freeze > requirements.txt

mkdir src tests

write code and tests
run webserver and tests to check.




-- Add Code to Git --

create new repo in github

add .gitignore

*.swp
**/*.egg-info
**/__pycache__
**/*.pyc
**/.cache/
**/.mypy_cache/
**.pytest_cache/
.python-version
venv
.env
.idea
.vs
package-lock.json


git init
git add requirements.txt setup.py src/main.py tests/test_main.py .gitignore

git commit -m "first commit"

git remote add origin git@github.com:sastels/python_talk.git

git push -u origin master




-- Heroku --


install Heroku cli

heroku login

pip install gunicorn and add to requirements.txt

Procfile:    web: gunicorn --pythonpath src main:App

heroku create

git push heroku master

heroku open


rename app in gui

git remote rm heroku
heroku git:remote -a python-talk-658




--  CI on Circle CI --

log into CircleCI and add github project

cut and paste the config.yml file

run build. it fails

fix config:
    use pytest rather than manage.py,
    pip install -e .




-- CD --


add .circleci/setup-heroku.sh

#!/bin/bash
git remote add heroku https://git.heroku.com/python-talk-658.git
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



append to config.yml

      - run: bash .circleci/setup-heroku.sh
      - add_ssh_keys:
          fingerprints:
            - "96:b5:99:a3:34:14:36:0c:21:75:37:16:0e:77:e5:f7"
      - deploy:
          name: Deploy Master to Heroku
          command: |
            if [ "${CIRCLE_BRANCH}" == "master" ]; then
              git push heroku master
            fi




set HEROKU_API_KEY and HEROKU_LOGIN in https://circleci.com/gh/sastels/python_talk/edit#env-vars

make new ssh key on terminal

add to circleci ssh permissions
hostname git.heroku.com
<private key>
put fingerprint in config.yml



add public key to

https://dashboard.heroku.com/account

(now the cds one)

