# What

Api to get latest version of jenkins plugins. Written i python 3.7

## Starting
pip install -r requirements
FLASK_APP=main flask run

or  with gunicorn
gunicorn -b 0.0.0.0:5000 -t 60 main:app

## Single plugin

curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5000\?plugin\=kubernetes


## Multi plugin

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"plugins": ["kubernetes", "git", "docker", "testlink"]}' \
  http://localhost:5000/multi


