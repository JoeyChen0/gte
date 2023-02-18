import glob
import sys
import numpy as np
import pandas as pd
import requests
import json
import webbrowser


def key(x):
    if (x[0] == '1'):
       return "Moves"
    return x.split(' "')[0][1:]

def val(x):
    if (x[0] == '1'):
        return x
    return x.split(' "')[1][:-2]

def parse(target):
    file = open(target, "r").read()
    games = file.split('\n\n\n')
    games = [i.split('\n') for i in games]
    return [{key(i): val(i) for i in game if i} for game in games]

def hide_time(moves):
    edited = ""
    clock = False
    for c in moves:
        if not clock:
            if c == '{':
                clock = True
            else:
                edited += c
        elif c == '}':
            clock = False
    return edited

def anonymise(game):
    chesscom = 'chess.com'
    lichess = 'lichess.org'

    if 'Chess.com' in game['Site']:
        chesscom = game['Link']
    else:
        lichess = game['Site']

    moves = hide_time(game['Moves'])

    return f'[White "{chesscom}"]\n[Black "{lichess}"]\n{moves}'

def import_game(game):
    pgn = anonymise(game)
    URL = 'https://lichess.org/api/import'
    r = requests.post(url=URL, data={'pgn': pgn})
    return json.loads(r.text)['url']


def main(args):
    files = glob.glob('**/*.pgn',recursive=True)
    all_games = sum([parse(file) for file in files], [])
    games_df = pd.DataFrame(all_games)

    num = 1
    if args:
        num = int(args[0])

    games = games_df.sample(num)

    for _,game in games.iterrows():
        url = import_game(game)
        webbrowser.open(url)


if __name__ == '__main__':
    main(sys.argv[1:])
