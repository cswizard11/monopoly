from Game import Game
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    monopoly = Game()
    return "Hello World"
    

#monopoly.setup()

#monopoly.play()