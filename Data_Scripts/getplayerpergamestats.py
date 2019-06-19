from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import playergamelog
import mysql.connector
import time
import numpy as np
import pandas as pd
from operator import itemgetter


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

# db = mysql.connector.connect(
#     host =  "d5x4ae6ze2og6sjo.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
#     user = "wbe5sn77tagogvdz",
#     passwd = "n9eckiq9qeyssuqy",
#     database = "pg3wk6oqwj8tellc"
# )

# db.set_converter_class(NumpyMySQLConverter)
# cursor = db.cursor()


#get teams
teams_dict = commonteamyears.CommonTeamYears()
teams_dict = teams_dict.team_years.get_dict()

teams = []
for teamNum in range(30):
    teams.append(teams_dict["data"][teamNum])

#get rosters
rosters = []
for team in teams:
    time.sleep(1)
    rosters_dict = commonteamroster.CommonTeamRoster(season="2018-19",team_id=team[1])
    rosters_dict = rosters_dict.common_team_roster.get_dict()
    rosters.append(rosters_dict["data"])


#get playerstats
leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame",season="2018-19")
leaguestats = leaguestats.league_dash_player_stats.get_dict()
leaguestats = leaguestats["data"]
leaguestats.sort(key = lambda x: x[0])
leaguestats_length = len(leaguestats)-1



for player in leaguestats:
    player_stats = playergamelog.PlayerGameLog(player_id = player[0], season = "2018-19")
    time.sleep(2)
    player_stats = player_stats.player_game_log.get_data_frame()
    path = 'Data_Scripts/playersCSV/' + str(player[0]) + "_" + str(player[1].replace(" ","-") + ".csv")
    player_stats.to_csv(path,index=False)
    print(player[1].replace(" ","-"))


# Deandre-Ayton
# Luka-Doncic
# Theo-Pinson
# Ray-Spalding
# Bonzie-Colson
# Vincent-Edwards