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

# export app variable
export FLASK_APP=app.py

# if needed you can activate the "development" environment e.g. for debugging purposes
export FLASK_ENV=development

# start app
flask run

# exit venv after you're done
deactivate
```

# Running tests
Make sure you are using `venv`, all dependencies are installed, 
then you can execute tests like this.
```
python -m pytest tests/
```
