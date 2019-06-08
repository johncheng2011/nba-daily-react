from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
import mysql.connector
import time
import numpy as np
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
class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    def _float64_to_mysql(self,value):
        return float(value)

db = mysql.connector.connect(
    host =  "d5x4ae6ze2og6sjo.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user = "wbe5sn77tagogvdz",
    passwd = "n9eckiq9qeyssuqy",
    database = "pg3wk6oqwj8tellc"
)
db.set_converter_class(NumpyMySQLConverter)
cursor = db.cursor()


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
leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="Totals",season="2018-19")
leaguestats = leaguestats.get_dict()
leaguestats = leaguestats["resultSets"][0]["rowSet"]
leaguestats.sort(key = lambda x: x[0])
leaguestats_length = len(leaguestats)-1

data = [] #fg%, ft%, 3p, reb, ast, stl, blk, pts, tov

fg_avg = fg_atm_avg = ft_avg = ft_atm_avg = fg3_avg = reb_avg = ast_avg = stl_avg = blk_avg = pts_avg = tov_avg = 0


temp = []
count = 0
for roster in rosters:
    for player in roster:
        pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
        temp.append(leaguestats[pos])
        count += 1
leaguestats = temp
for player in leaguestats:
    try:
        fg_avg += player[12]
        fg_atm_avg += player[11]/player[5]
        ft_avg += player[18]
        ft_atm_avg += player[17]/player[5]
        fg3_avg += player[13]/player[5]
        reb_avg += player[21]/player[5]
        ast_avg += player[22]/player[5]
        stl_avg += player[24]/player[5]
        blk_avg += player[25]/player[5]
        pts_avg += player[29]/player[5]
        tov_avg += player[23]/player[5]
    except:
        continue
length = len(leaguestats)

fg_avg = fg_avg/length
fg_atm_avg = fg_atm_avg/length
ft_avg = ft_avg/length
fg_atm_avg = ft_atm_avg/length
fg3_avg = fg3_avg/length
reb_avg = reb_avg/length
ast_avg = ast_avg/length
stl_avg = stl_avg/length
blk_avg = blk_avg/length
pts_avg = pts_avg/length
tov_avg = tov_avg/length


data = []
for player in leaguestats:
    try:
        
        insert_fg = (player[12] - fg_avg) * (player[11]/player[5])
        insert_ft = (player[18] - fg_avg) * (player[17]/player[5])
        insert_fg3 = player[13]/player[5]
        insert_reb = player[21]/player[5]
        insert_ast = player[22]/player[5]
        insert_stl = player[24]/player[5]
        insert_blk = player[25]/player[5]
        insert_pts = player[29]/player[5]
        insert_tov = player[23]/player[5]

        insert = [insert_fg, insert_ft, insert_fg3, insert_reb, insert_ast, insert_stl, insert_blk, insert_pts, insert_tov]
        
        data.append(insert) 

    except:
        continue
avg = np.average(data, axis = 0)
std = np.std(data,axis = 0)

zscores = []

for index in range(len(leaguestats)):
    
    fgz = round((data[index][0]-avg[0])/std[0],2)
    ftz = round((data[index][1]-avg[1])/std[1],2)
    fg3z = round((data[index][2]-avg[2])/std[2],2)
    rebz = round((data[index][3]-avg[3])/std[3],2)
    astz = round((data[index][4]-avg[4])/std[4],2)
    stlz = round((data[index][5]-avg[5])/std[5],2)
    blkz = round((data[index][6]-avg[6])/std[6],2)
    ptsz = round((data[index][7]-avg[7])/std[7],2)
    tovz = round((data[index][8]-avg[8])/std[8],2)
    mins = round(leaguestats[index][9]/leaguestats[index][5],1)
    gp = leaguestats[index][5]
    total = round(fgz + ftz + fg3z + rebz + astz + stlz + blkz + ptsz - tovz,2)
    insert = [leaguestats[index][1],leaguestats[index][0],leaguestats[index][2],leaguestats[index][3],gp,mins,fgz,ftz,fg3z,rebz,astz,stlz,blkz,ptsz,tovz,total]
    zscores.append(insert)
zscores.sort(key = lambda x:x[15])
for player in zscores:
    print(player)
    

sql = "CREATE TABLE IF NOT EXISTS playerstatsz (playerid INT, playername VARCHAR(255), teamid INT, teamabbr VARCHAR(20),gp INT,min DECIMAL(4,1) , fgz DECIMAL(4,2), ftz DECIMAL(4,2), fg3z DECIMAL(4,2), rebz DECIMAL(4,2), astz DECIMAL(4,2), stlz DECIMAL(4,2), blkz DECIMAL(4,2), ptsz DECIMAL(4,2), tovz DECIMAL(4,2), total DECIMAL(4,2), PRIMARY KEY (playerid))"
cursor.execute(sql)

pruneSQL = "DELETE FROM playerstatsz WHERE NOT("



for player in zscores:
    sql = "INSERT INTO playerstatsz (playerid, playername, teamid, teamabbr, gp, min, fgz, ftz, fg3z, rebz, astz, stlz, blkz, ptsz, tovz, total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, min = %s, fgz = %s, ftz = %s, fg3z = %s, rebz = %s, astz = %s, stlz = %s, blkz = %s, ptsz = %s, tovz = %s, total = %s"
    values = (player[1],player[0],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12],player[13],player[14],player[15],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12],player[13],player[14],player[15])
    prt = sql%(values)
    cursor.execute(sql,values)
    pruneSQL += "(playerid=%s)OR"%(player[1])
    db.commit()

pruneSQL = pruneSQL[:-2]#remove last OR
pruneSQL += ")"#add closing )
cursor.execute(pruneSQL)
db.commit()
db.disconnect()


# for roster in rosters:
#     for player in roster:
#         pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
#         playerstats = leaguestats[pos]
#         sql = "INSERT INTO playerstest (playerid, playername, teamid, teamabbr,gp,win,loss,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,treb,ast,stl,blk,pts,tov,fouls) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, win = %s, loss = %s, min = %s, fgm = %s, fga = %s, fg_pct = %s, fg3m = %s, fg3a = %s, fg3_pct = %s, ftm = %s, fta = %s, ft_pct = %s, oreb = %s, dreb = %s, treb = %s, ast = %s, stl = %s, blk = %s, pts= %s, tov = %s, fouls = %s"
#         values = (playerstats[0],playerstats[1],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27])
#         #prt = sql%(values)
#         #print(prt)
#         cursor.execute(sql,values)
#         pruneSQL += "(playerid=%s)OR"%(playerstats[0])
#         db.commit()


# pruneSQL = pruneSQL[:-2]#remove last OR
# pruneSQL += ")"#add closing )
# cursor.execute(pruneSQL)
# db.commit()
# db.disconnect()




# print("league ft attps avg " + str(league_ft_apg_avg))
# print("league ft avg " + str(league_ft_avg))

# for player in leaguestats:
#     weighted_ft = (player[18] - league_ft_avg) * (player[17]/player[5])/ league_ft_apg_avg
#     insert = [player[1],weighted_ft]
#     weighted.append(insert)

# print(weighted[0])
# weighted.sort(key = lambda x : x[1])
# print(type(weighted[0]))



#pruneSQL = "DELETE FROM playerstest WHERE NOT("

# for roster in rosters:
#     for player in roster:
#         pos = binarySearch(leaguestats,0,leaguestats_length,player[12])
#         playerstats = leaguestats[pos]
#         sql = "INSERT INTO playerstest (playerid, playername, teamid, teamabbr,gp,win,loss,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,treb,ast,stl,blk,pts,tov,fouls) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         sql += " ON DUPLICATE KEY UPDATE teamid = %s, teamabbr = %s, gp = %s, win = %s, loss = %s, min = %s, fgm = %s, fga = %s, fg_pct = %s, fg3m = %s, fg3a = %s, fg3_pct = %s, ftm = %s, fta = %s, ft_pct = %s, oreb = %s, dreb = %s, treb = %s, ast = %s, stl = %s, blk = %s, pts= %s, tov = %s, fouls = %s"
#         values = (playerstats[0],playerstats[1],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27],playerstats[2],playerstats[3],playerstats[5],playerstats[6],playerstats[7],playerstats[9],playerstats[10],playerstats[11],playerstats[12],playerstats[13],playerstats[14],playerstats[15],playerstats[16],playerstats[17],playerstats[18],playerstats[19],playerstats[20],playerstats[21],playerstats[22],playerstats[24],playerstats[25],playerstats[29],playerstats[23],playerstats[27])
#         #prt = sql%(values)
#         #print(prt)
#         cursor.execute(sql,values)
#         pruneSQL += "(playerid=%s)OR"%(playerstats[0])
#         db.commit()


# pruneSQL = pruneSQL[:-2]#remove last OR
# pruneSQL += ")"#add closing )
# cursor.execute(pruneSQL)
# db.commit()
# db.disconnect()