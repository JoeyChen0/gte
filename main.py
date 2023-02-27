from glob import glob
from pandas import DataFrame
from requests import post
from json import loads
import webbrowser
from re import findall
from random import choice

MIN_MOVES = 10


def key(x):
    if (x[0] != '['):
        return "Moves"
    return x.split(' "')[0][1:]


def val(x):
    if (x[0] != '['):
        return hide_time(x)
    try:
        return x.split(' "')[1][:-2]
    except IndexError:
        print(x)
        raise Exception


def parse(target):
    file = open(target, "r").read()
    games = file.split('\n\n\n')
    games = [i.split('\n') for i in games]
    return [{key(i): val(i) for i in game if i} for game in games]


def game_length(moves):
    result = findall(r'\d+\.', moves)
    if (not result):
        return 0
    return int(result[-1][0:-1])


def filter_games(games, min_moves):
    return games[games['Moves'].map(game_length) > min_moves]


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

    moves = game['Moves']
    white = game['White']
    black = game['Black']

    return f'[Event "{white} vs {black}"]\n[White "{chesscom}"]\n[Black "{lichess}"]\n[Annotator "Joey"]\n{moves}{{ test }}'


def import_game(game):
    pgn = anonymise(game)
    URL = 'https://lichess.org/api/import'
    r = post(url=URL, data={'pgn': pgn})
    return loads(r.text)['url']


def main():
    files = glob('**/*.pgn', recursive=True)
    games = [filter_games(DataFrame(parse(file)),MIN_MOVES) for file in files]

    game = choice(games).sample().squeeze()
    url = import_game(game)
    webbrowser.open(url)


if __name__ == '__main__':
    main()
