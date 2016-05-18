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
        if name not in self.players:
            self.players.append(name)
    
    def add_game(self, p1, p2, h, a):
        if any(p1 == g.p1 and p2 == g.p2 for g in self.games):
            return "Game already played!"
        else:
            self.games.append(Game(p1, p2, h, a))
            return "Game not played yet"

app = Flask(__name__)

tournaments = []

@app.route('/')
def root():
    return render_template("index.html")  
    
"""
Creates a new game 
"""   
@app.route('/api/new/tournament')
def new_tournament():
    tournaments.append(Tournament())
    return "new tournament added"
    
"""
Adds a player to the current tournament
"""
@app.route('/api/new/player/<name>')
def new_player(name):
    tournaments[-1].add_player(name)
    return "new player %s added" % name

"""
Plays a game
"""
@app.route('/api/new/game')
def new_game():
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')
    f = request.args.get('home_points')
    a = request.args.get('away_points')
    tournaments[-1].add_game(p1, p2, f, a)
    return "new game played"    

@app.route('/game/<int:num>')
def show_game(num):
    assert num <= len(games)
    return render_template('game.html', game=games[num])        
          
if __name__ == '__main__':
    app.run(debug=True)