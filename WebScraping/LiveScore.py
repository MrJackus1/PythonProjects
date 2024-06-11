#Create a program which will return whatever live football matches are playing. Professional level.
'''
This program scrapes the 'live' api request, which then returns a json string. We can then parse this with .json
query the data and return what ever we want :)
'''
import requests,json

url = "https://www.sofascore.com/api/v1/sport/football/events/live"

def getScores(urll):    
    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, utf-8",
        "Referer": "https://www.sofascore.com/",
        "X-Requested-With": "84a546",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "If-None-Match": "W/b24054250d",
        "Priority": "u=4",
        "Cache-Control": "max-age=0",
        "TE": "trailers"
    }
    response = requests.request("GET", urll, data=payload, headers=headers)    
    jsonStuff = response.text
    
    return json.loads(jsonStuff)

def liveScore(jsondata): 
    padding = '----------------------------------------------------------------------------------'
    liveMatches = len(jsondata['events'])
    xxx = (f'''There are {liveMatches} live games currently.\n{padding}\n''')
    for events in jsondata['events']:        
        leagueName = events['tournament']['name']
        homeTeam = events['homeTeam']['name']
        awayTeam = events['awayTeam']['name']
        homeScore = events['homeScore']['current']
        awayScore = events['awayScore']['current']
        matchTime = events['tournament']['name']
        comment = events['status']['description']
        xxx += f'''{leagueName}: {homeTeam} ({homeScore} ~ {awayScore}) {awayTeam}  -: {comment}\n'''
    xxx += f'{padding}'
    return xxx

print(liveScore(getScores(url)))
    



