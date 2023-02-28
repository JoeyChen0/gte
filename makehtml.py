from enum import Enum


class Site(Enum):
    LICHESS = 0
    CHESSCOM = 1


class AmbResult(Enum):
    TIME = 'lost on time'
    RESIGN = 'resigned'
    UNKNOWN = 'Unknown'


def get_site(game):
    if 'Chess.com' in game['Site']:
        return Site.CHESSCOM
    return Site.LICHESS


def get_embed(url):
    id = url.split('/')[-1]
    return f'https://lichess.org/embed/game/{id}'


def get_link(game, site):
    if site == Site.CHESSCOM:
        return game['Link']
    return game['Site']


def get_termination(game, site):

    termination = None

    if '#' in game['Moves']:
        return 'Checkmate'

    elif 'time' in game['Termination']:
        termination = 'lost on time'

    else:
        termination = 'resigned'

    match game['Result']:
        case '1-0':
            return f'Black{termination}'
        case '0-1':
            return f'White{termination}'
        case _:
            return 'Draw'


def get_time_control(game, site):
    if game['TimeControl'] in ['15+0', '30+0']:
        return 'UltraBullet'
    if game['TimeControl'] in ['60', '60+0', '60+1', '120', '120+1']:
        return 'Bullet'
    if game['TimeControl'] in ['180', '180+0', '180+2', '300', '300+0', '300+2', '300+3', '300+5']:
        return 'Blitz'
    if game['TimeControl'] in ['600', '600+0', '600+5', '900+10', '900+15', '1800']:
        return 'Rapid'
    if game['TimeControl'] in ['1800+0', '1800+20']:
        return 'Classical'
    return 'Daily'


def chesscom_tc(game):
    return game['TimeControl']


def lichess_tc(game):
    return game['TimeControl']


def makepage(path, game, url):
    game_src = get_embed(url)
    white = game['White']
    black = game['Black']
    players = f'{white} v {black}'
    site = get_site(game)
    link = get_link(game, site)
    termination = get_termination(game, site)
    time_control = get_time_control(game, site)

    TEMPLATE = f'''<!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" href="style.css">
        <script src=util.js></script>

    </head>

    <body>
        <div style="width: 60%; height:100%; margin-left: 10%; float: left;">
            <iframe src="{game_src}"></iframe>
        </div>
        <div style="margin-left: 70%">
            <input type="button" style="margin-top: 10%" id="players_button" onclick="reveal('players_button', '{players}')"
                value="Show Answer"></button>
            <br>
            <input type=button class="btn btn-success" onclick=" window.open('{link}','_blank')"
                value=Link></input>
            <br>
            <input type="button" id="term_button" onclick="reveal('term_button', '{termination}')"
                value="Show Termination"></input>
            <br>
            <input type="button" id="time_control_button" value="Show Time Control" onclick="reveal('time_control_button', '{time_control}')"></input>
        </div>
    </body>

    </html>'''

    with open(path, 'w') as file:
        file.write(TEMPLATE)
