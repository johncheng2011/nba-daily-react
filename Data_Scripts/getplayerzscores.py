from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
import mysql.connector
import time
import numpy as np
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
    time.sleep(1)
    rosters_dict = commonteamroster.CommonTeamRoster(season=season,team_id=team[1])
    rosters_dict = rosters_dict.common_team_roster.get_dict()
    rosters.append(rosters_dict["data"])


#get playerstats
leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame",season=season)
leaguestats = leaguestats.league_dash_player_stats.get_dict()
leaguestats = leaguestats["data"]
leaguestats.sort(key = lambda x: x[0])
leaguestats_length = len(leaguestats)-1

#only use players on rosters
temp = []
for roster in rosters:
    for player in roster:
        pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
        temp.append(leaguestats[pos])
leaguestats = temp

#order of per game stats array
# fg
# ft
# fg3
# reb
# ast
# stl
# blk
# pts
# tov

#get desired stats
per_game_stats = [itemgetter(12,18,13,21,22,24,25,29,23)(leaguestats[i]) for i in range(len(leaguestats))]

#make numpy array
np_stats = np.array(per_game_stats)

#get avg league fg and ft
average_per_game = np.average(np_stats[:,:2],axis=0)
fg_avg = average_per_game[0]
fg_atm_avg = average_per_game[1]

#calculate weighted fg and ft
for i in range(len(leaguestats)):  
    np_stats[i][0] = (leaguestats[i][12] - fg_avg) * (leaguestats[i][11])
    np_stats[i][1] = (leaguestats[i][18] - fg_avg) * (leaguestats[i][17])

#get league avg and std for each stat
avg = np.average(np_stats, axis = 0)
std = np.std(np_stats,axis = 0)

#calculate zscores for each player and stat
zscores = []
for index in range(len(leaguestats)):
    
    fgz = np.around((np_stats[index][0]-avg[0])/std[0],decimals = 2)
    ftz = np.around((np_stats[index][1]-avg[1])/std[1],decimals = 2)
    fg3z = np.around((np_stats[index][2]-avg[2])/std[2],decimals = 2)
    rebz = np.around((np_stats[index][3]-avg[3])/std[3],decimals = 2)
    astz = np.around((np_stats[index][4]-avg[4])/std[4],decimals = 2)
    stlz = np.around((np_stats[index][5]-avg[5])/std[5],decimals = 2)
    blkz = np.around((np_stats[index][6]-avg[6])/std[6],decimals = 2)
    ptsz = np.around((np_stats[index][7]-avg[7])/std[7],decimals = 2)
    tovz = np.around((np_stats[index][8]-avg[8])/std[8],decimals = 2)
    mins = np.around(leaguestats[index][9],decimals = 1)
    gp = leaguestats[index][5]
    total = np.around(fgz + ftz + fg3z + rebz + astz + stlz + blkz + ptsz - tovz,decimals = 2)
    insert = [leaguestats[index][1],leaguestats[index][0],leaguestats[index][2],leaguestats[index][3],gp,mins,fgz,ftz,fg3z,rebz,astz,stlz,blkz,ptsz,tovz,total]
    zscores.append(insert)


zscores.sort(key = lambda x:x[15])

for player in zscores:
    print(player)


#create table if not exist
sql = "CREATE TABLE IF NOT EXISTS playerstatsz"+season_split+" (playerid INT, playername VARCHAR(255), teamid INT, teamabbr VARCHAR(20),gp INT,min DECIMAL(4,1) , fgz DECIMAL(4,2), ftz DECIMAL(4,2), fg3z DECIMAL(4,2), rebz DECIMAL(4,2), astz DECIMAL(4,2), stlz DECIMAL(4,2), blkz DECIMAL(4,2), ptsz DECIMAL(4,2), tovz DECIMAL(4,2), total DECIMAL(4,2), PRIMARY KEY (playerid))"
cursor.execute(sql)

#pruneSQL for getting rid of players in table but no longer on active rosters
pruneSQL = "DELETE FROM playerstatsz"+season_split+" WHERE NOT("

#add player into table
for player in zscores:
    sql = "INSERT INTO playerstatsz"+season_split+" (playerid, playername, teamid, teamabbr, gp, min, fgz, ftz, fg3z, rebz, astz, stlz, blkz, ptsz, tovz, total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, min = %s, fgz = %s, ftz = %s, fg3z = %s, rebz = %s, astz = %s, stlz = %s, blkz = %s, ptsz = %s, tovz = %s, total = %s"
    values = (player[1],player[0],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12],player[13],player[14],player[15],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12],player[13],player[14],player[15])
    prt = sql%(values)
    cursor.execute(sql,values)
    pruneSQL += "(playerid=%s)OR"%(player[1])
    db.commit()

#execute pruneSQL
pruneSQL = pruneSQL[:-2]#remove last OR
pruneSQL += ")"#add closing )
cursor.execute(pruneSQL)
db.commit()
db.disconnect()

