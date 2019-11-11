import mysql.connector
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify, make_response,send_file
import json
import database
from decimal import Decimal
from flask_cors import CORS
import random
from datetime import date
app = Flask(__name__,template_folder='./reactfrontend/build', static_folder='./reactfrontend/build/static')
CORS(app)

app.config['SECRET_KEY'] = database.secretkey



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
app.json_encoder = DecimalEncoder

@app.route('/_allPlayerPerGame',methods=['GET'])
def perGame():
    db = database.connectDB('2019-20')
    cursor = db.cursor(dictionary = True)

    cursor.execute("SELECT * FROM playerstats201920")

    stats = cursor.fetchall()
    return jsonify(stats)

@app.route('/_allPlayerZscores',methods=['GET'])
def zscores():
    db = database.connectDB('2019-20')
    cursor = db.cursor(dictionary = True)

    cursor.execute("SELECT * FROM playerstatsz201920")

    stats = cursor.fetchall()
    return jsonify(stats)


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/logo192.png')
def image():
    return send_file('./reactfrontend/build/logo192.png',mimetype='image/png')

@app.route('/_players/<date>',methods=['GET'])
def playersPerGameStats(date):
    # db = database.connectDB('2019-20')
    # cursor = db.cursor(dictionary = True)

    # cursor.execute("SELECT * FROM playerstats201920")

    # stats = cursor.fetchall()
    # return jsonify(stats)

    year,month,day = date.split('-')

    if(int(month) > 8):
        season = year+'-'+str((int(year)+1)%100)
    else:
        season = str(int(year)-1)+'-'+str(int(year)%100)
    season_split = season.replace('-','')

    db = database.connectDB(season)
    mycursor = db.cursor(dictionary=True)
    mycursor.execute('SELECT * FROM games'+season_split+' WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []

    for game in games:
        mycursor.execute('SELECT * FROM playerstats'+season_split+' WHERE(teamid = '+ str(game['teamid']) +')')
        players += mycursor.fetchall()
    players.sort(key= lambda x: x['pts'], reverse=True)
    db.disconnect()
    return jsonify(players)

@app.route('/_zscores/<date>',methods=['GET'])
def playersZscoresStats(date):
    year,month,day = date.split('-')

    if(int(month) > 8):
        season = year+'-'+str((int(year)+1)%100)
    else:
        season = str(int(year)-1)+'-'+str(int(year)%100)
    season_split = season.replace('-','')


    db = database.connectDB(season)
    mycursor = db.cursor(dictionary=True)
    mycursor.execute('SELECT * FROM games'+season_split+' WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        
        mycursor.execute('SELECT * FROM playerstatsz'+season_split+' WHERE(teamid = '+ str(game['teamid']) +')')
        players += mycursor.fetchall()
    db.disconnect()
    players.sort(key = lambda x: x['total'],reverse=True)
    return jsonify(players)


@app.route('/_allZScores',methods=['GET'])
def allPlayersZ():
    db = database.connectDB('2019-20')
    cursor = db.cursor(dictionary = True)

    cursor.execute("SELECT * FROM playerstatsz201920")

    stats = cursor.fetchall()
    db.disconnect()
    stats.sort(key = lambda x: x['total'], reverse = True)
    return jsonify(stats)

@app.route('/_allPerGame',methods=['GET'])
def allPlayersPerGame():
    db = database.connectDB('2019-20')
    cursor = db.cursor(dictionary = True)

    cursor.execute("SELECT * FROM playerstats201920")

    stats = cursor.fetchall()
    db.disconnect()
    stats.sort(key = lambda x: x['pts'], reverse = True)
    return jsonify(stats)

@app.route('/_rand_player',methods=['GET'])
def randPlayer():
    db = database.connectDB('2019-20')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM playerstats201920")
    playersPerGame = cursor.fetchall()
    player = random.randint(0,len(playersPerGame))
    cursor.execute("SELECT * FROM playerstatsz201920 WHERE(playerid = %s)"%(playersPerGame[player]['playerid']))
    playersZscores = cursor.fetchone()
    retPlayer = {'perGame': playersPerGame[player], 'zScore':playersZscores }
    db.disconnect()
    return jsonify(retPlayer)


@app.route('/_today_games',methods=['GET'])
def todayGames():
    today = date.today()
    db = database.connectDB('2019-20')
    mycursor = db.cursor(dictionary = True)
    today = today.strftime('%Y-%m-%d')
    mycursor.execute('SELECT matchup FROM games201920 WHERE(gamedate = STR_TO_DATE("'+ str(today) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    db.disconnect()
    #remove duplicates
    seen = set()
    new_games = []
    for d in games:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_games.append(d)



    return jsonify(new_games)

@app.route('/test/<player>')
def test(player):
    db = database.connectDB('2019-20')
    mycursor = db.cursor(dictionary= True)
    mycursor.execute("SELECT * FROM playergamelog201920 WHERE(playerid = %s)" %(player))
    games = mycursor.fetchall()
    fg_pct = {}
    ft_pct = {}
    fg3m = {}
    reb = {}
    ast = {}
    stl = {}
    blk = {}
    pts = {}
    tov = {}
    chartList = [fg_pct,ft_pct,fg3m,reb,ast,stl,blk,pts,tov]
    fg_pct['title'] = "Field Goal Percentage"
    ft_pct['title'] = "Free Throw Percentage"
    fg3m['title'] = "Three Pointers Made"
    reb['title'] = " Rebounds"
    ast['title'] = "Assists"
    stl['title'] = "Steals"
    blk['title'] = "Blocks"
    pts['title'] = "Points"
    tov['title'] = "Turnovers"

    for chart in chartList:
        chart['axis'] = {
            'x':{
                'type':'category',
                'categories':[]
            },
            'y':{}
        }
        chart['data'] = {
            'columns':[['data1']],
            'type':'line',
            'names':{'data1':chart['title']}
        }
        chart['axis']['x']['show'] = False
        chart['axis']['y']['min'] = 0
    fg_pct['axis']['y']['max'] = 1
    ft_pct['axis']['y']['max'] = 1
    fg_pct['axis']['y']['padding'] = {'top':0,'bottom':0}
    ft_pct['axis']['y']['padding'] = {'top':0,'bottom':0}
    for game in games:
        gamedate = date.strftime(game['gamedate'],'%m/%d/%Y')
        fg_pct['data']['columns'][0].append(game['fg_pct'])
        ft_pct['data']['columns'][0].append(game['ft_pct'])
        fg3m['data']['columns'][0].append(game['fg3m'])
        reb['data']['columns'][0].append(game['reb'])
        ast['data']['columns'][0].append(game['ast'])
        stl['data']['columns'][0].append(game['stl'])
        blk['data']['columns'][0].append(game['blk'])
        pts['data']['columns'][0].append(game['pts'])
        tov['data']['columns'][0].append(game['tov'])
        for chart in chartList:
            chart['axis']['x']['categories'].append(gamedate)

    return jsonify(chartList)
@app.route('/players/<date>')
def playersPerGame(date):
    return render_template('index.html')

@app.route('/zscores/<date>')
def playersZscores(date):
    return render_template('index.html')

@app.route('/<about>')
def about(about):
    print(about)
    return render_template('index.html')