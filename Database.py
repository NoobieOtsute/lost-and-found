import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE lostItems (
  #  itemName text,
  #  category text,
  #  dateFound text,
  #  locationFound text
#  )""")

# c.execute("""CREATE TABLE users (
  #  username text,
  #  password text
#  )""")

  
def searchItem(item):
  c.execute("SELECT * from lostItems WHERE itemName=?",(item,))
  conn.commit()
  print(c.fetchall())

def addItem(item,category,date,location):
  c.execute("INSERT INTO lostItems (itemName,category,dateFound,locationFound) VALUES (?,?,?,?)",(item,category,date,location))
  conn.commit()

def addUser(username,password):
  c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
  conn.commit()

def searchUser(username,password):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * from users WHERE username=? AND password=?",(username,password,))
  conn.commit()
  info = c.fetchall()
  conn.close()
  return info

def listItemCategory():
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * from lostItems ORDER BY category")
  items = c.fetchall()
  conn.close()
  return items

# addItem('sweater', 'clothing', '27/2/2023', 'WEC')
# addUser('Otsute', '123')

print(listItemCategory())



conn.close()
