import mysql.connector
from nba_api.stats.endpoints import leaguegamelog
game = leaguegamelog.LeagueGameLog()
game = game.get_dict()
mydb = mysql.connector.connect(
    host =  "d5x4ae6ze2og6sjo.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user = "wbe5sn77tagogvdz",
    passwd = "n9eckiq9qeyssuqy",
    database = "pg3wk6oqwj8tellc"
)
mycursor = mydb.cursor()
#mycursor.execute("DROP TABLE games")
mycursor.execute("CREATE TABLE IF NOT EXISTS games (season INT, teamid INT, teamname VARCHAR(20),gamedate DATE, matchup VARCHAR (255), gameid INT)")
for games in game["resultSets"][0]["rowSet"]:
    sql = "INSERT INTO games(season,teamid,teamname,gamedate,matchup,gameid) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (games[0],games[1],games[3],games[5],games[6],games[4])
    mycursor.execute(sql,val)
mydb.commit()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)
#mycursor.execute("CREATE TABLE games (season INT, teamid INT, teamname VARCHAR(255), gamedate DATE, matchup VARCHAR(255), gameid INT)")
