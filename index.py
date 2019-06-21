from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, RadioField
from flask_wtf import FlaskForm
import mysql.connector
import json
from decimal import Decimal
from datetime import datetime, timedelta
from Data_Scripts import database
from flask_cors import CORS
import pandas as pd
import time
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'asdf3234bdfe'



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def tomDate(date):
    dateObj = datetime.strptime(date,'%Y-%m-%d')
    dateObj += timedelta(days=1)
    dateStr = datetime.strftime(dateObj, '%Y-%m-%d')
    return dateStr
app.jinja_env.filters['tomorrowDate'] = tomDate

def yesDate(date):
    dateObj = datetime.strptime(date,'%Y-%m-%d')
    dateObj -= timedelta(days=1)
    dateStr = datetime.strftime(dateObj, '%Y-%m-%d')
    return dateStr
app.jinja_env.filters['yesterdayDate'] = yesDate


class date(FlaskForm):
    enterDate = DateField('dateInput',format = '%Y-%m-%d',default=datetime(2018,10,16))
    selectType = RadioField("Data Type", choices=[('1','per-game'),('2','zscores')],default='1')
    submit = SubmitField('submit')


@app.route("/", methods=['POST','GET'])
def index():
    form = date()
    if form.validate_on_submit():
        if(form.selectType.data == '1'):
            inDate = form.enterDate.data
            
            return redirect(url_for('players',date=inDate))
        else:
            return redirect(url_for('playerzscores',date=form.enterDate.data))
    return render_template('index.html',form = form,title="home")




@app.route("/games")
def games():
    return render_template('games.html')

@app.route("/all_players")
def all_players():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    players = []
    
    mycursor.execute('SELECT * FROM playerstats')
    players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return render_template('all_players.html',players=players)


@app.route("/all_players_zscores")
def all_playersz():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    players = []
    
    mycursor.execute('SELECT * FROM playerstatsz')
    players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return render_template('all_players_zscores.html',players=players)


@app.route("/players/<date>")
def players(date):
    
    return render_template('players.html',date=date)


@app.route("/players_zscores/<date>")
def playerzscores(date):
    
    return render_template('players_zscores.html',players=players,date=date)



@app.route("/_players/<date>")
def playerdata(date):
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        mycursor.execute('SELECT * FROM playerstats WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

@app.route("/_players_zscores/<date>")
def getplayerszscores(date):
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        
        mycursor.execute('SELECT * FROM playerstatsz WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

@app.route("/<player>")
def player_page(player):
    name,id = player.split('_')
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    sql = 'SELECT * FROM playergamelog WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    gamelog = mycursor.fetchall()
    sql = 'SELECT * FROM playerstats WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    pergame = mycursor.fetchall()
    sql = 'SELECT * FROM playerstatsz WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    zscore = mycursor.fetchall()
    return render_template('player_page.html', gamelog=gamelog, pergame=pergame,zscore=zscore)

@app.route("/teams")
def teams():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
    )
    mycursor = db.cursor()
    teams = ['Atlanta_Hawks', 'Boston_Celtics', 'Brooklyn_Nets', 'Charlotte_Hornets', 'Chicago_Bulls', 'Cleveland_Cavaliers', 'Dallas_Mavericks', 'Denver_Nuggets', 'Detroit_Pistons', 'Golden_State_Warriors', 'Houston_Rockets', 'Indiana_Pacers', 'Los_Angeles_Clippers', 'Los_Angeles_Lakers', 'Menphis_Grizzlies', 'Miami_Heat', 'Milwaukee_Bucks', 'Minnesota_Timberwolves', 'New_Orleans_Pelicans', 'New_York_Knicks', 'Oklahoma_City_Thunder', 'Orlando_Magic', 'Philadelphia_76ers', 'Phoenix_Suns', 'Portland_Trail_Blazers', 'Sacramento_Kings', 'San_Antonio_Spurs', 'Toronto_Raptors', 'Utah_Jazz', 'Washington_Wizards']
    rosters = []
    players = {}
    for team in teams:
        sql = "SELECT * FROM " + team + "_Roster"
        mycursor.execute(sql)
        rosters = mycursor.fetchall()
        sql = "SELECT * FROM playerstats WHERE(teamid = " + str(rosters[0][0]) + ") ORDER BY pts DESC"
        mycursor.execute(sql)
        players[team] = mycursor.fetchall()


    return render_template('teams.html', rosters=players)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
