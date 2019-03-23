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

# To activate auto-reloading on file changes
export FLASK_DEBUG=1

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

# Adding/removing dependencies
To add dependencies use pip.
```
pip install Flask-Assets
```

After that you have to update `requirements.txt`.
```
pip freeze > requirements.txt
```

If you remove any dependency you have to update `requirements.txt` as well.
```
pip uninstall Flask-Assets
pip freeze > requirements.txt
```