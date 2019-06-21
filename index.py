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
from nba_api.stats.endpoints import commonteamyears
from nba_api.stats.endpoints import commonteamroster
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

@app.route("/asdf")
def player_page():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM playergamelog WHERE(playerid=2544) ')
    gamelog = mycursor.fetchall()
    mycursor.execute('SELECT * FROM playerstats WHERE(playerid=2544) ')
    pergame = mycursor.fetchall()
    mycursor.execute('SELECT * FROM playerstatsz WHERE(playerid=2544) ')
    zscore = mycursor.fetchall()
    return render_template('player_page.html', gamelog=gamelog, pergame=pergame,zscore=zscore)

@app.route("/teams")
def teams():
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
    return render_template('teams.html', rosters=rosters)
if __name__ == "__main__":
    app.run(host='0.0.0.0')