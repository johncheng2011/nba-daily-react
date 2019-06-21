import mysql.connector
from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
import time
import database


num_to_team = {1610612737:"Atlanta_Hawks",1610612738:"Boston_Celtics", 1610612739:"Cleveland_Cavaliers", 1610612740:"New_Orleans_Pelicans", 1610612741:"Chicago_Bulls", 1610612742: "Dallas_Mavericks",1610612743:"Denver_Nuggets", 1610612744:"Golden_State_Warriors",1610612745:"Houston_Rockets", 1610612746:"Los_Angeles_Clippers", 1610612747: "Los_Angeles_Lakers", 1610612748: "Miami_Heat",1610612750:"Minnesota_Timberwolves", 1610612751:"Brooklyn_Nets", 1610612752:"New_York_Knicks", 1610612753:"Orlando_Magic", 1610612754: "Indiana_Pacers", 1610612755: "Philadelphia_76ers", 1610612756:"Phoenix_Suns", 1610612757:"Portland_Trail_Blazers", 1610612758:"Sacramento_Kings",1610612759:"San_Antonio_Spurs", 1610612760:"Oklahoma_City_Thunder", 1610612749:"Milwaukee_Bucks", 1610612762:"Utah_Jazz", 1610612763:"Menphis_Grizzlies",1610612764:"Washington_Wizards", 1610612765:"Detroit_Pistons", 1610612766:"Charlotte_Hornets", 1610612761:"Toronto_Raptors"}
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

db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
cursor = db.cursor()

for team in teams:
    sql = "CREATE TABLE IF NOT EXISTS "
    sql += str(num_to_team[team[1]]) + "_Roster (teamid INT, playerid INT, playername VARCHAR(255), num INT, position VARCHAR(255), height VARCHAR(255), weight INT, age INT, PRIMARY KEY (playerid))"
    cursor.execute(sql)
    print(num_to_team[team[1]])

for roster in rosters:
    pruneSQL = "DELETE FROM "+ num_to_team[roster[0][0]] +"_Roster WHERE NOT("
    for player in roster:
        sql = "INSERT INTO " + num_to_team[player[0]] + "_Roster(teamid,playerid,playername,num,position,height,weight,age) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql += "ON DUPLICATE KEY UPDATE num = %s, position = %s, height = %s, weight = %s, age = %s"
        values = (player[0],player[12],player[3],player[4],player[5],player[6],player[7],player[9],player[4],player[5],player[6],player[7],player[9])
        pruneSQL += "(playerid=%s)OR"%(player[12])
        cursor.execute(sql,values)
        db.commit()
    pruneSQL = pruneSQL[:-2]#remove last OR
    pruneSQL += ")"#add closing )
    cursor.execute(pruneSQL)
    db.commit()


# [1610612761, '2018', '00', 'Pascal Siakam', '43', 'F', '6-9', '230', 'APR 02, 1994', 25.0, '2', 'New Mexico State', 1627783]

