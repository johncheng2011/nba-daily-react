from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
import mysql.connector
import time


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


db = mysql.connector.connect(
    host =  "d5x4ae6ze2og6sjo.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user = "wbe5sn77tagogvdz",
    passwd = "n9eckiq9qeyssuqy",
    database = "pg3wk6oqwj8tellc"
    )

cursor = db.cursor()
#create table
sql = "CREATE TABLE IF NOT EXISTS playerstats (playerid INT, playername VARCHAR(255), teamid INT, teamabbr VARCHAR(10), gp INT, win INT,loss INT,"
sql += "min DECIMAL(3,1), fgm DECIMAL(3,1), fga DECIMAL(3,1), fg_pct DECIMAL(4,3), fg3m DECIMAL(3,1), fg3a DECIMAL(3,1), fg3_pct DECIMAL(4,3), ftm DECIMAL(3,1), fta DECIMAL(3,1), ft_pct DECIMAL(4,3), oreb DECIMAL(3,1), dreb DECIMAL(3,1),"
sql += "treb DECIMAL(3,1), ast DECIMAL(3,1), stl DECIMAL(3,1), blk DECIMAL(3,1), pts DECIMAL(3,1), tov DECIMAL(3,1), fouls DECIMAL(3,1), PRIMARY KEY(playerid) )"
cursor.execute(sql)

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

#pruneSQL for getting rid of players in table but no longer on active rosters
pruneSQL = "DELETE FROM playerstats WHERE NOT("

#add each player to table
for roster in rosters:
    for player in roster:
        pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
        playerstats = leaguestats[pos]
        sql = "INSERT INTO playerstats (playerid, playername, teamid, teamabbr,gp,win,loss,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,treb,ast,stl,blk,pts,tov,fouls) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, win = %s, loss = %s, min = %s, fgm = %s, fga = %s, fg_pct = %s, fg3m = %s, fg3a = %s, fg3_pct = %s, ftm = %s, fta = %s, ft_pct = %s, oreb = %s, dreb = %s, treb = %s, ast = %s, stl = %s, blk = %s, pts= %s, tov = %s, fouls = %s"
        values = (playerstats[0],playerstats[1],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27])
        cursor.execute(sql,values)
        pruneSQL += "(playerid=%s)OR"%(playerstats[0])
        db.commit()

#execute pruneSQL
pruneSQL = pruneSQL[:-2]#remove last OR
pruneSQL += ")"#add closing )
cursor.execute(pruneSQL)
db.commit()
db.disconnect()