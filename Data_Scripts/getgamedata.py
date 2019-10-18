import mysql.connector
from nba_api.stats.endpoints import leaguegamelog
import database
season = '2019-20'
game = leaguegamelog.LeagueGameLog(season=season)
game = game.get_dict()




mydb = database.connectDB(season)
mycursor = mydb.cursor()

# create table and add game data for each game
season = ''.join(season.split('-'))
mycursor.execute("CREATE TABLE IF NOT EXISTS games"+season+" (season INT, teamid INT, teamname VARCHAR(255),gamedate DATE, matchup VARCHAR (255), gameid INT)")
for games in game["resultSets"][0]["rowSet"]:
    sql = "INSERT INTO games"+ season +" (season,teamid,teamname,gamedate,matchup,gameid) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (games[0],games[1],games[3],games[5],games[6],games[4])
    mycursor.execute(sql,val)
mydb.commit()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)