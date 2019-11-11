import mysql.connector
databaseInfo = dict(
    host =  'nbastats.csbgdmytwgow.us-east-1.rds.amazonaws.com',
    user = 'admin',
    passwd = 'WMYWlftGMwleL7qSjwWZ',
    database = 'nbadata')

secretkey = '9OCN2IXQRYFCY3CthRkS'


def connectDB(season):
    return  mysql.connector.connect(
        host =  databaseInfo["host"],
        user = databaseInfo["user"],
        passwd = databaseInfo["passwd"],
        database = 'season' + ''.join(season.split('-'))
    )

