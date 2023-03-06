import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE lostItems (
#    id integer,
#    itemName text,
#    category text,
#    dateFound text,
#    locationFound text,
#    detail text,
#    imageName text
#  )""")

# c.execute("""CREATE TABLE users (
#    username text,
#    password text
#  )""")

  
def searchItem(item):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * from lostItems WHERE itemName=?",(item,))
  conn.commit()
  list = c.fetchall()
  # print(list)
  conn.close()
  return list

def deleteItem(id):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("DELETE FROM lostItems WHERE id=?",(id))
  conn.commit()
  conn.close()

def addItem(id,item,category,date,location,detail,image):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("INSERT INTO lostItems (id,itemName,category,dateFound,locationFound,detail,imageName) VALUES (?,?,?,?,?,?,?)",(id,item,category,date,location,detail,image))
  conn.commit()
  conn.close()

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

def listItemDate():
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * from lostItems ORDER BY dateFound")
  items = c.fetchall()
  conn.close()
  return items

def listItemLocation():
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * from lostItems ORDER BY locationFound")
  items = c.fetchall()
  conn.close()
  return items

def LastID():
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("SELECT * FROM lostItems WHERE id=(SELECT max(id) FROM lostItems)")
  ID = c.fetchall()
  conn.close()
  return ID

# addItem(0,'books', 'stationary', '27/2/2023', 'WEC', 'blue, small')
# addItem(1,'pen', 'stationary', '26/2/2023', 'SB', 'black')
# addItem(2,'bag', 'bag', '26/2/2023', 'SB', 'adidas', r'D:\Users\Otsute\VScode\LostAndFound\LostAndFound\Images\bag.jpg')
# addItem(3,'hat', 'clothing', '28/2/2023', 'SC', 'nike', r'D:\Users\Otsute\VScode\LostAndFound\LostAndFound\Images\hat.png')
# addItem(4,'sweater', 'clothing', '27/2/2023', 'WEC', 'champion')


# addUser('Otsute', '123')
# print(searchItem('Nike Hat'))
# print(listItemCategory())

conn.close()