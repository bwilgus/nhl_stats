import requests
from pprint import pprint as pp
import pandas as pd


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

## Rink
bounds = {'x':[-100.0,100.0]
          ,'y':[-45.0,45.0]
          }
goals = [-89.0,89.0]
# 0.0,0.0 is center ice


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
play_data = []

for yr in range(2018,2019):
    print(yr)
    for g in range(381,1272):
        print(g)

        game = '000' + str(g)
        game_id = str(yr) + '02' + game[len(game)-4:]


        r = requests.get('https://statsapi.web.nhl.com/api/v1/game/' + game_id + '/feed/live')
        plays = r.json()['liveData']['plays']['allPlays']


        headers = [
            'game_id'
            ,'period'
            ,'time_left'
            ,'away_score'
            ,'home_score'
            ,'event'
            ,'description'
            ,'secondary_event'
            ,'x'
            ,'y'
            ,'player_1'
            ,'player_1_id'
            ,'player_1_team'
            ,'player_1_team_id'
            ,'player_1_type'
            ,'player_2'
            ,'player_2_id'
            ,'player_2_team'
            ,'player_2_team_id'
            ,'player_2_type'
            ]

        i = 0

        for p in plays:
            if i % 50 == 0:
                print(i)
            try:
                opp_team = {r.json()['gameData']['teams']['away']['triCode']:r.json()['gameData']['teams']['home']['triCode']
                            ,r.json()['gameData']['teams']['away']['id']:r.json()['gameData']['teams']['home']['id']
                            ,r.json()['gameData']['teams']['home']['triCode']:r.json()['gameData']['teams']['away']['triCode']
                            ,r.json()['gameData']['teams']['home']['id']:r.json()['gameData']['teams']['away']['id']
                            }
            except:
                opp_team = {r.json()['gameData']['teams']['away']['abbreviation']:r.json()['gameData']['teams']['home']['abbreviation']
                            ,r.json()['gameData']['teams']['away']['id']:r.json()['gameData']['teams']['home']['id']
                            ,r.json()['gameData']['teams']['home']['abbreviation']:r.json()['gameData']['teams']['away']['abbreviation']
                            ,r.json()['gameData']['teams']['home']['id']:r.json()['gameData']['teams']['away']['id']
                            }

                
            if (p['result']['event'] == 'Game Scheduled') or (p['result']['event'] == 'Period Ready') or (p['result']['event'] == 'Period Start'):
                continue
            else:
                period = p['about']['period']
                time_left = p['about']['periodTimeRemaining']
                away_score = p['about']['goals']['away']
                home_score = p['about']['goals']['home']
                event = p['result']['event']
                description = p['result']['description']
                
                try:
                    sec_event = p['result']['secondaryType']
                except:
                    sec_event = ''
                try:
                    x = p['coordinates']['x']
                    y = p['coordinates']['y']
                except:
                    x = ''
                    y = ''
                try:
                    player_1 = p['players'][0]['player']['fullName']
                    player_1_id = p['players'][0]['player']['id']
                    player_1_team = p['team']['triCode']
                    player_1_team_id = p['team']['id']
                except:
                    player_1 = ''
                    player_1_id = ''
                    player_1_team = ''
                    player_1_team_id = ''
                try:
                    player_1_type = p['players'][0]['playerType']
                except:
                    player_1_type = ''
                try:
                    player_2 = p['players'][1]['player']['fullName']
                    player_2_id = p['players'][1]['player']['id']
                    player_2_team = opp_team[player_1_team]
                    player_2_team_id = opp_team[player_1_team_id]
                    player_2_type = p['players'][1]['playerType']
                except:
                    player_2 = ''
                    player_2_id = ''
                    player_2_team = ''
                    player_2_team_id = ''
                    player_2_type = ''
                
                play_data.append([
                    game_id
                    ,period
                    ,time_left
                    ,away_score
                    ,home_score
                    ,event
                    ,description
                    ,sec_event
                    ,x
                    ,y
                    ,player_1
                    ,player_1_id
                    ,player_1_team
                    ,player_1_team_id
                    ,player_1_type
                    ,player_2
                    ,player_2_id
                    ,player_2_team
                    ,player_2_team_id
                    ,player_2_type
                    ])
                    

                i += 1

df = pd.DataFrame(play_data,columns=headers)
