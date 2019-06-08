import mysql.connector
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2
import numpy as np
import statistics
from datetime import datetime
import database
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

# a = ["hello",1,2,3,4]
# b = [["asdf",1,2333,332],["asdf",2,3432,34],["asdf",3,234,3],["asdf",4,2343,32]]
# #print(np.std(a))
# print(np.std(b[1],axis = 0))



# a = []
# b = {'name':'test name', 'ft_pct': .554}
# a.append(b)



# def binarySearch(arr,l,r,target):
#     while l<=r:
#         mid = int(l+(r-l)/2)

#         if (arr[mid][0] == target):
#             return mid
#         elif (arr[mid][0] < target):
#             l = mid + 1
#         else:
#             r = mid -1
#     return -1


# stats = playerprofilev2.PlayerProfileV2(player_id=1628381, per_mode36="PerGame")
# stats = stats.get_dict()
# index = len(stats["resultSets"][0]["rowSet"])
# print(stats["resultSets"][0]["rowSet"][index-1])

# leaguestats = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed="PerGame",season="2018-19")
# leaguestats = leaguestats.get_dict()
# print(leaguestats["resultSets"][0]["headers"])
# leaguestats = leaguestats["resultSets"][0]["rowSet"]
# leaguestats.sort(key = lambda x: x[0])

# print(binarySearch(leaguestats,0,len(leaguestats)-1,leaguestats[53][0]))
# print(leaguestats[2])






# [[1610612737, '2018', '00', 'Justin Anderson', '1', 'G-F', '6-6', '230', 'NOV 19, 1993', 25.0, '3', 'Virginia', 1626147], [1610612737, '2018', '00', 'Kevin Huerter', '3', 'G', '6-7', '190', 'AUG 27, 1998',
# 20.0, 'R', 'Maryland', 1628989], [1610612737, '2018', '00', 'Deyonta Davis', '4', 'C-F', '6-11', '237', 'DEC 02, 1996', 22.0, '2', 'Michigan State', 1627738], [1610612737, '2018', '00', 'Omari Spellman', '6', 'F', '6-9', '245', 'JUL 21, 1997', 21.0, 'R', 'Villanova', 1629016], [1610612737, '2018', '00', 'Isaac Humphries', '8', 'C', '7-0', '260', 'JAN 05, 1998', 21.0, 'R', 'Kentucky', 1629353], [1610612737, '2018', '00', 'Jaylen Adams', '10', 'G', '6-2', '190', 'MAY 04, 1996', 23.0, 'R', 'St. Bonaventure', 1629121], [1610612737, '2018', '00', 'Trae Young', '11', 'G', '6-2', '180', 'SEP 19, 1998', 20.0, 'R', 'Oklahoma', 1629027], [1610612737, '2018', '00', 'Taurean Prince', '12', 'F', '6-8', '220', 'MAR 22, 1994', 25.0, '2', 'Baylor', 1627752], [1610612737, '2018', '00', 'Dewayne Dedmon', '14', 'C', '7-0', '245', 'AUG 12, 1989', 29.0, '5', 'Southern California', 203473], [1610612737, '2018', '00', 'Vince Carter', '15', 'F-G', '6-6', '220', 'JAN 26, 1977', 42.0, '20', 'North Carolina', 1713], [1610612737, '2018', '00', 'Miles Plumlee', '18', 'C', '6-11', '249', 'SEP 01, 1988', 30.0, '6', 'Duke', 203101], [1610612737, '2018', '00', 'John Collins', '20', 'F-C', '6-10', '235', 'SEP 23, 1997', 21.0, '1', 'Wake Forest', 1628381], [1610612737, '2018', '00', 'Alex Poythress', '22', 'F', '6-9', '235', 'SEP 06, 1993', 25.0, '2', 'Kentucky', 1627816], [1610612737, '2018', '00', 'Kent Bazemore', '24', 'G', '6-5', '201', 'JUL 01, 1989', 29.0, '6', 'Old Dominion', 203145], [1610612737, '2018', '00', 'Alex Len', '25', 'C', '7-1', '250', 'JUN 16, 1993', 25.0, '5', 'Maryland', 203458], [1610612737, '2018', '00', "DeAndre' Bembry", '95', 'F', '6-6', '210', 'JUL 04, 1994', 24.0, '2', "Saint Joseph's", 1627761]]
# [[1610612737, '2018', '00', 'Justin Anderson', '1', 'G-F', '6-6', '230', 'NOV 19, 1993', 25.0, '3', 'Virginia', 1626147], [1610612737, '2018', '00', 'Kevin Huerter', '3', 'G', '6-7', '190', 'AUG 27, 1998',
# 20.0, 'R', 'Maryland', 1628989], [1610612737, '2018', '00', 'Deyonta Davis', '4', 'C-F', '6-11', '237', 'DEC 02, 1996', 22.0, '2', 'Michigan State', 1627738], [1610612737, '2018', '00', 'Omari Spellman', '6', 'F', '6-9', '245', 'JUL 21, 1997', 21.0, 'R', 'Villanova', 1629016], [1610612737, '2018', '00', 'Isaac Humphries', '8', 'C', '7-0', '260', 'JAN 05, 1998', 21.0, 'R', 'Kentucky', 1629353], [1610612737, '2018', '00', 'Jaylen Adams', '10', 'G', '6-2', '190', 'MAY 04, 1996', 23.0, 'R', 'St. Bonaventure', 1629121], [1610612737, '2018', '00', 'Trae Young', '11', 'G', '6-2', '180', 'SEP 19, 1998', 20.0, 'R', 'Oklahoma', 1629027], [1610612737, '2018', '00', 'Taurean Prince', '12', 'F', '6-8', '220', 'MAR 22, 1994', 25.0, '2', 'Baylor', 1627752], [1610612737, '2018', '00', 'Dewayne Dedmon', '14', 'C', '7-0', '245', 'AUG 12, 1989', 29.0, '5', 'Southern California', 203473], [1610612737, '2018', '00', 'Vince Carter', '15', 'F-G', '6-6', '220', 'JAN 26, 1977', 42.0, '20', 'North Carolina', 1713], [1610612737, '2018', '00', 'Miles Plumlee', '18', 'C', '6-11', '249', 'SEP 01, 1988', 30.0, '6', 'Duke', 203101], [1610612737, '2018', '00', 'John Collins', '20', 'F-C', '6-10', '235', 'SEP 23, 1997', 21.0, '1', 'Wake Forest', 1628381], [1610612737, '2018', '00', 'Alex Poythress', '22', 'F', '6-9', '235', 'SEP 06, 1993', 25.0, '2', 'Kentucky', 1627816], [1610612737, '2018', '00', 'Kent Bazemore', '24', 'G', '6-5', '201', 'JUL 01, 1989', 29.0, '6', 'Old Dominion', 203145], [1610612737, '2018', '00', 'Alex Len', '25', 'C', '7-1', '250', 'JUN 16, 1993', 25.0, '5', 'Maryland', 203458], [1610612737, '2018', '00', "DeAndre' Bembry", '95', 'F', '6-6', '210', 'JUL 04, 1994', 24.0, '2', "Saint Joseph's", 1627761]]




db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)

print(db)
mycursor = db.cursor()
mycursor.execute("SELECT * FROM playerstats")
players = mycursor.fetchall()
for player in players:
    print(player)
