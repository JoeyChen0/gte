import os
import glob
import numpy as np
import pandas as pd


def parse(fle):
    x = open(fle, "r").read()
    y = x.split('\n\n\n')
    z = [yy.split('\n') for yy in y]
    a = lambda b: '[MOVES "'+b+'"]' if b[0] == '1' else b
    c = [[a(zzz) for zzz in zz if len(zzz) > 3] for zz in z]
    d = lambda e: e.split(' "')[0][1:]
    f = lambda g: g.split(' "')[1][:-2]
    h = [{d(ccc): f(ccc) for ccc in cc} for cc in c if len(cc)]
    return h


# directory = 'pgn/'
# files = os.listdir(directory)
files = glob.glob('**/*.pgn',recursive=True)
all_games = sum([parse(file) for file in files], [])
games_df = pd.DataFrame(all_games)
print(all_games)
# games_df['_cl'] = games_df['Site']
# games_df['_cl'][games_df['Site'] != 'Chess.com'] = 'Lichess'
# games_df['_bbr'] = 'Other'
# games_df['_bbr'][games_df['TimeControl'].isin(['60', '60+0', '60+1', '120', '120+1'])] = 'Bullet'
# games_df['_bbr'][games_df['TimeControl'].isin(['180', '180+0', '180+2', '300', '300+0', '300+2', '300+5'])] = 'Blitz'
# games_df['_bbr'][games_df['TimeControl'].isin(['600', '600+0', '600+5', '900+15', '1800'])] = 'Rapid'
# print(games_df.groupby(['_bbr', '_cl']).count())