from flask import Flask, render_template

app = Flask(__name__)
app.static_folder = 'assets'

@app.route('/')
def hello_world():
    return render_template('page_1.html')

@app.route('/page-2')
def page_2():
    return render_template('page_2.html')