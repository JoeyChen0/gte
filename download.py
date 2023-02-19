
import requests
import sys 
import getopt
import time
import datetime
from dateutil.relativedelta import relativedelta
import re

lichess_URL = 'https://lichess.org/api/games/user/hikaru'

USAGE_MSG =  '''\
usage: download.py <args> <username> 
    optional args:
        -l <username>       lichess
        -c <username>       chesscom
        -f <filename>       download path
        -d --duration <x>   number of months
        --start <date>      start date (format: dd/mm/yy)
'''

LICHESS_EPOCH = 1356998400070
EPOCH = datetime.datetime.utcfromtimestamp(0).date()

def add_months(date, duration):
    return date + relativedelta(months=duration)

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def get_date_range(start, duration):
    end = datetime.date.today()
    if (start is None):
        if (duration is None):
            duration = 0
        start = add_months(end, -duration)

    elif (duration is not None):
        end = min(end,add_months(start, duration))

    return (start,end)

def date_to_timestamp(date):
    return max(int((date - EPOCH).total_seconds() * 1000), LICHESS_EPOCH)

def write_to_file(r, path):
    if 200 <= r.status_code < 300:
        with open(path, 'ab') as file:
            file.write(r._content)
    else:
        print(f'status code: {r.status_code} - {r.reason} | {r.url}')

def get_lichess_pgns(username, date_range, path):
    url = f'https://lichess.org/api/games/user/{username}'
    since = date_to_timestamp(date_range[0])
    until = date_to_timestamp(date_range[1])
    params = {
        'since': since,
        'until': until,
        'evals': False
    }
    r = requests.get(url=url, params=params)
    write_to_file(r, path)

    
def get_chesscom_urls(username, date_range):
    date = date_range[0]
    urls = []
    while (date <= date_range[1]):
        month = str(date.month) if date.month >= 10 else f'0{date.month}'
        urls.append(f'https://api.chess.com/pub/player/{username}/games/{date.year}/{month}/pgn')
        date = add_months(date, 1)
    return urls

def get_chesscom_pgns(username, date_range, path):
    urls = get_chesscom_urls(username, date_range)
    for url in urls:
        r = requests.get(url)
        write_to_file(r, path)
    
def main(opts, args):
    filename = f'{time.time()}.pgn'

    chesscom = None
    lichess = None
    start = None
    duration = None
    
    if (args):
        chesscom = args[0]

    for o,a in opts:
        if o == '-l':
            lichess = a
        elif o == '-c':
            chesscom = a
        elif o=='-f':
            if (re.search('.*\.pgn', a)):
                filename = a
            else:
                filename = f'{a}/{filename}'
        elif o == '-d' or o == '--duration':
            duration = int(a)
        elif o == '-s' or o == '--start':
            start = datetime.datetime.strptime(a, "%d/%m/%y").date()

    if (lichess is None and chesscom is None):
        print(USAGE_MSG)
        return
    
    date_range = get_date_range(start, duration)
    if (lichess):
        get_lichess_pgns(username=lichess, date_range=date_range, path=filename)
    if (chesscom):
        get_chesscom_pgns(username=chesscom, date_range=date_range, path=filename)
    

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, ":c:l:f:d:m:s:h", longopts=["start=", "duration="])
        main(opts, args)
        
    except getopt.GetoptError as error:
        print(error.msg)