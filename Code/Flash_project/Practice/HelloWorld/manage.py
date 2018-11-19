from flask import Flask
from flask_script import Manager

app = Flask(__name__)

manager = Manager(app=app)

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    manager.run()

