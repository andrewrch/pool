#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request
"""
tourament
{
    players:
    [
        "ac"    
    ]
    games:
    [
        
    ]
}
"""

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
        
class Game:
    def __init__(self, p1, p2, h, a):
        self.p1 = p1
        self.p2 = p2
        self.home = h
        self.away = a

class Tournament:
    def __init__(self):
        self.players = []
        self.games = []
        
    def add_player(self, name):
        if name in self.players:
            raise InvalidUsage('Player already in tournament', status_code=500)   
        self.players.append(name)
        return "Player %s added" % name
    
    def add_game(self, p1, p2, h, a):
        if any(p1 == g.p1 and p2 == g.p2 for g in self.games):
            raise InvalidUsage('Game already played', status_code=500)   
        self.games.append(Game(p1, p2, h, a))
        return "Added game"

app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

tournaments = []

def add_tournament():
    global tournaments
    tournaments.append(Tournament())   
    return "Added tournament"
     
def add_game(p1, p2, h, a):
    global tournaments
    if len(tournaments) < 1:
        raise InvalidUsage('Create a tournament first', status_code=500)    
        
    return tournaments[-1].add_game(p1, p2, h, a)
    
def add_player(name):
    global tournaments
    if len(tournaments) < 1:
        raise InvalidUsage('Create a tournament first', status_code=500)
        
    return tournaments[-1].add_player(name)
    
@app.route('/')
def root():
    return render_template("index.html")  
    
"""
Creates a new game 
"""   
@app.route('/api/new/tournament')
def new_tournament():
    add_tournament()
    return "new tournament added"
    
"""
Adds a player to the current tournament
"""
@app.route('/api/new/player/<name>')
def new_player(name):
    add_player(name)    
    return "new player %s added" % name

"""
Plays a game
"""
@app.route('/api/new/game')
def new_game():
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')
    h = request.args.get('home_points')
    a = request.args.get('away_points')
    add_game(p1, p2, h, a)
    return "new game played"    

@app.route('/game/<int:num>')
def show_game(num):
    assert num <= len(games)
    return render_template('game.html', game=games[num]) 
    
@app.route('/slack', methods=['POST'])
def slack():
    words = request.form['text'].split(' ')
    command = words[0]
    if command == "add":
        type = words[1]
        if type == "tournament":
            return add_tournament()
        elif type == "game":
            return add_game(words[2], words[3], words[4], words[5])
        elif type == "player":
            return add_player(words[2])
    else:
        raise InvalidUsage('Invalid command', status_code=500)                     
          
if __name__ == '__main__':
    app.run(debug=True)