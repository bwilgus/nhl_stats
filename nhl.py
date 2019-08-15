import requests
from pprint import pprint as pp

## API Docs = https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md

def teams_get():
    return requests.get('http://statsapi.web.nhl.com/api/v1/teams')

def single_team_get(team_id):
    return requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + str(team_id))

def player_get(player_id):
    return requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(player_id))

def player_season_stats(player_id, season):
    return requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(player_id) + '?statsSingleSeason&season=' + str(season))

def season_schedule(year_start,year_end):
    return requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(year_start) + '-08-01&endDate=' + str(year_end) + '-07-31')


## Game Structure
year = '2019' #stands for the year beginning, ex: 2018 = 2018-2019
type_of_game = {'preseason':'01'
                ,'regular season':'02'
                ,'playoffs':'03'
                ,'allstar':'04'
                }
game_number = '0001'
# Regular Season is 0001 through either 1271 (2017 - Present) or 1230 (pre-2017, 30 teams)
# Playoffs
## 2nd digit is playoff round
## 3rd digit denotes which series
## 4th digit denotes which game
## ex: 0217 = 2nd round, 1st matchup, 7th game


## Test game

r = requests.get('https://statsapi.web.nhl.com/api/v1/game/2018020001/feed/live')

