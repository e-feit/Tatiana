# Requirements
* python3

# Installation
Create new `venv` and install dependencies.
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

# Starting application
```
# activate venv if not done yet
. venv/bin/activate

# start app
export FLASK_APP=app.py
flask run

# exit venv
deactivate
```
