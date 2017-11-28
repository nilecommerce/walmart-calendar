from flask import Flask

app = Flask('bambi-engine')

@app.route('/')
def hello_world():
    return "Hello World"
