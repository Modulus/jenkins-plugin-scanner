# What

Api to get latest version of jenkins plugins. Written i python 3.7

## Starting
pip install -r requirements@
FLASK_APP=main flask run


## Single plugin

curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5000\?plugin\=kubernetes


## Multi plugin

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"plugins": ["kubernetes", "git", "docker", "testlink"]}' \
  http://localhost:5000/multi


