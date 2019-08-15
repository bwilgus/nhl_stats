import requests
from pprint import pprint as pp

def get_draft(year):
    return requests.get('https://statsapi.web.nhl.com/api/v1/draft/' + str(year))

def get_prospects(year):
    return requests.get('https://statsapi.web.nhl.com/api/v1/draft/prospects?year=' + str(year))

def single_prospect(ID):
    return requests.get('https://statsapi.web.nhl.com/api/v1/draft/prospects/' + str(ID))

