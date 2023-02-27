import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE lostItems (
  #  itemName text,
  #  category text
#  )""")

# c.execute("""CREATE TABLE users (
  #  username text,
  #  password text
#  )""")

  
def searchItem(item):
  c.execute("SELECT * from lostItems WHERE itemName=?",(item,))
  conn.commit()
  print(c.fetchall())

def addItem(item,category):
  c.execute("INSERT INTO lostItems (itemName,category) VALUES (?,?)",(item,category))
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

# addItem('hat', 'clothing')
# addUser('Otsute', '123')


conn.close()
