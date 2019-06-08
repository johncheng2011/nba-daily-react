from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
import mysql.connector
import time

# def binarySearch(arr, l, r, target):
#     if r>=1:
#         m = int(l+(r-l)/2)
#         if(arr[m][0] == target):
#             return m
#         elif(arr[m][0]>target ):
#             return binarySearch(arr,l,m-1,target)
#         else:
#             return binarySearch(arr, m+1,r,target)
#     else:
#         return -1

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
sql = "CREATE TABLE IF NOT EXISTS playerstats (playerid INT, playername VARCHAR(255), teamid INT, teamabbr VARCHAR(10), gp INT, win INT,loss INT,"
sql += "min DECIMAL(3,1), fgm DECIMAL(3,1), fga DECIMAL(3,1), fg_pct DECIMAL(4,3), fg3m DECIMAL(3,1), fg3a DECIMAL(3,1), fg3_pct DECIMAL(4,3), ftm DECIMAL(3,1), fta DECIMAL(3,1), ft_pct DECIMAL(4,3), oreb DECIMAL(3,1), dreb DECIMAL(3,1),"
sql += "treb DECIMAL(3,1), ast DECIMAL(3,1), stl DECIMAL(3,1), blk DECIMAL(3,1), pts DECIMAL(3,1), tov DECIMAL(3,1), fouls DECIMAL(3,1), PRIMARY KEY(playerid) )"
cursor.execute(sql)
#get teams
teams_dict = commonteamyears.CommonTeamYears()
teams_dict = teams_dict.get_dict()
teams = []
for teamNum in range(30):
    teams.append( teams_dict["resultSets"][0]["rowSet"][teamNum])

#get rosters
rosters = []
for team in teams:
    time.sleep(1)
    rosters_dict = commonteamroster.CommonTeamRoster(season="2018-19",team_id=team[1])
    rosters_dict = rosters_dict.get_dict()
    rosters.append(rosters_dict["resultSets"][0]["rowSet"])

#get playerstats
leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame",season="2018-19")
leaguestats = leaguestats.get_dict()
leaguestats = leaguestats["resultSets"][0]["rowSet"]
leaguestats.sort(key = lambda x: x[0])
leaguestats_length = len(leaguestats)-1

pruneSQL = "DELETE FROM playerstats WHERE NOT("

for roster in rosters:
    for player in roster:
        pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
        playerstats = leaguestats[pos]
        sql = "INSERT INTO playerstats (playerid, playername, teamid, teamabbr,gp,win,loss,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,treb,ast,stl,blk,pts,tov,fouls) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, win = %s, loss = %s, min = %s, fgm = %s, fga = %s, fg_pct = %s, fg3m = %s, fg3a = %s, fg3_pct = %s, ftm = %s, fta = %s, ft_pct = %s, oreb = %s, dreb = %s, treb = %s, ast = %s, stl = %s, blk = %s, pts= %s, tov = %s, fouls = %s"
        values = (playerstats[0],playerstats[1],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27])
        
        #prt = sql%(values)
        #print(prt)
        cursor.execute(sql,values)
        pruneSQL += "(playerid=%s)OR"%(playerstats[0])
        db.commit()


pruneSQL = pruneSQL[:-2]#remove last OR
pruneSQL += ")"#add closing )
cursor.execute(pruneSQL)
db.commit()
db.disconnect()
# for team in teams["resultSets"][0]["rowSet"]:
#     print(team) 
#[2037, 'Jamal Crawford', 1610612756, 'PHX', 39.0, 64, 13, 51, 0.203, 18.9, 2.7, 6.8, 0.397, 1.0, 3.2, 0.332, 1.5, 1.7, 0.845, 0.1, 1.2, 1.3, 3.6, 1.5, 0.5, 0.2, 0.1, 1.2, 1.4, 7.9, -5.9, 15.5, 0, 0, 201, 374, 17, 494, 271, 257, 224, 415, 181, 167, 264, 174, 201, 81, 480, 438, 452, 80, 108, 277, 338, 438, 398, 224, 229, 517, 261, 261, 38, 5, '2037,1610612756']
#             
# 
# 
# 
# 
# 
            # "PLAYER_ID",
            # "PLAYER_NAME",
            # "TEAM_ID",
            # "TEAM_ABBREVIATION",
            # "AGE",
            # "GP",
            # "W",
            # "L",
            # "W_PCT",
            # "MIN",
            # "FGM",
            # "FGA",
            # "FG_PCT",
            # "FG3M",
            # "FG3A",
            # "FG3_PCT",
            # "FTM",
            # "FTA",
            # "FT_PCT",
            # "OREB",
            # "DREB",
            # "REB",
            # "AST",
            # "TOV",
            # "STL",
            # "BLK",
            # "BLKA",
            # "PF",
            # "PFD",
            # "PTS",
            # "PLUS_MINUS",
            # "NBA_FANTASY_PTS",
            # "DD2",
            # "TD3",
            # "GP_RANK",
            # "W_RANK",
            # "L_RANK",
            # "W_PCT_RANK",
            # "MIN_RANK",
            # "FGM_RANK",
            # "FGA_RANK",
            # "FG_PCT_RANK",
            # "FG3M_RANK",
            # "FG3A_RANK",
            # "FG3_PCT_RANK",
            # "FTM_RANK",
            # "FTA_RANK",
            # "FT_PCT_RANK",
            # "OREB_RANK",
            # "DREB_RANK",
            # "REB_RANK",
            # "AST_RANK",
            # "TOV_RANK",
            # "STL_RANK",
            # "BLK_RANK",
            # "BLKA_RANK",
            # "PF_RANK",
            # "PFD_RANK",
            # "PTS_RANK",
            # "PLUS_MINUS_RANK",
            # "NBA_FANTASY_PTS_RANK",
            # "DD2_RANK",
            # "TD3_RANK",
            # "CFID",
            # "CFPARAMS"