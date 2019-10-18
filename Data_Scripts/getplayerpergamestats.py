from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import playergamelog
import mysql.connector
import time
import numpy as np
import pandas as pd
import datetime
from operator import itemgetter
import database


season = '2018-19'
season_split = ''.join(season.split('-'))

def binarySearch(arr,l,r,target):
    while l<=r:
        mid = int(l+(r-l)/2)

        if (arr[mid][0] == target):
            return mid
        elif (arr[mid][0] < target):
            l = mid + 1
        else:
            r = mid -1
    return -1

class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    def _float64_to_mysql(self,value):
        return float(value)
db = database.connectDB(season)

db.set_converter_class(NumpyMySQLConverter)
cursor = db.cursor()


#get teams
teams_dict = commonteamyears.CommonTeamYears()
teams_dict = teams_dict.team_years.get_dict()

teams = []
for teamNum in range(30):
    teams.append(teams_dict["data"][teamNum])

#get rosters
rosters = []
for team in teams:
    time.sleep(.5)
    rosters_dict = commonteamroster.CommonTeamRoster(season=season,team_id=team[1])
    rosters_dict = rosters_dict.common_team_roster.get_dict()
    rosters.append(rosters_dict["data"])


#get playerstats
leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame",season=season)
leaguestats = leaguestats.league_dash_player_stats.get_dict()
leaguestats = leaguestats["data"]
leaguestats.sort(key = lambda x: x[0])
leaguestats_length = len(leaguestats)-1

sql = "CREATE TABLE IF NOT EXISTS playergamelog"+season_split+" (seasonid INT, playerid INT, gameid INT, gamedate DATE, matchup VARCHAR(255), win VARCHAR(255),min INT,"
sql += "fgm INT, fga INT, fg_pct DECIMAL(4,3), fg3m INT, fg3a INT, fg3_pct DECIMAL(4,3), ftm INT, fta INT, ft_pct DECIMAL(4,3), oreb INt, dreb INT, reb INT,"
sql += "ast INT, stl INT, blk INT, tov INT, pf INT, pts INT, plusminus INT, PRIMARY KEY (playerid, gamedate))"
cursor.execute(sql)

for player in leaguestats:
    player_stats = playergamelog.PlayerGameLog(player_id = player[0], season = season)
    time.sleep(1)
    player_stats = player_stats.player_game_log.get_data_frame()
    for index, game in player_stats.iterrows():
        sql = "INSERT INTO playergamelog"+season_split+" (seasonid,playerid,gameid,gamedate,matchup,win,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,reb,ast,stl,blk,tov,pf,pts,plusminus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE seasonid = %s"
        values = ()
        for i in range(len(game)-1):
            if(i == 3):
                game[i] = datetime.datetime.strptime(game[i],'%b %d, %Y')
            values = values + (game[i],)
        values = values + (game[0],)
        cursor.execute(sql,values)
        db.commit()

