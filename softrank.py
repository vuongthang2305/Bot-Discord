import sqlite3 as lite
import os
import sys

class user():
    id = 0
    lvl = 1
    exp = 0
    name = ""
    def __init__(self,id , level = 1, exp = 0,name = ""):
        self.id = id
        self.lvl = level
        self.exp = exp
        self.name = name

def select(query):
    con = None
    
    try:
        path = os.path.dirname(__file__) + "\\database\\dbuser.db"
        con = lite.connect(path)
        
        cur = con.cursor()    
        cur.execute(query)
        while True:
        
            data = cur.fetchall()
            if data == None:
                return None
            return data
    except lite.Error as e:
        print ("Error %s:" % e.args[0])
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()

datas = select('select* from user where id ="9002"')


Luser = []

for data in datas:
    Luser.append(user(data[0],data[1],data[2],data[3]))

for i in range(len(Luser)):
    for j in range(len(Luser)):
        if i != j:
            if Luser[i].lvl == Luser[j].lvl:
                if Luser[i].exp > Luser[j].exp:
                        temp = Luser[i]
                        Luser[i] = Luser[j]
                        Luser[j] = temp
            elif Luser[i].lvl > Luser[j].lvl:
                temp = Luser[i]
                Luser[i] = Luser[j]
                Luser[j] = temp

for i in Luser:
    print(i.lvl, i.name)