import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="gamesdb"
)
gameList = []

with open('./GameLibrary-All/steamgames.csv', 'r', encoding="utf8") as file:
  csvreader = csv.reader(file)
  for n, row in enumerate(csvreader):
    appid = row[0]
    name = row[1]
    tags = row[10]
    developer = row[4]
    val = (n, appid, name, tags, developer)
    if n <= 10000 and n!= 0:
        gameList.append(val)

mycursor = mydb.cursor()
sql = "INSERT INTO games (`id`, `appid`, `name`, `tags`, `developer`) VALUES (%s, %s, %s, %s, %s)"
try:  
    mycursor.executemany(sql, gameList)
    print(mycursor.rowcount, "records inserted.")
except:
  print('Something went wrong.')

mydb.commit()


