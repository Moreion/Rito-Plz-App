
import requests
import os
import requestsEngine
import spreadsheetEngine
import staticRequests
import sqlite3
import databaseEngine

conn = sqlite3.connect('rito.db')
c = conn.cursor()

# --El programa--

def main():
    user = (str)(raw_input('\nType your User Name here: '))

    c.execute("SELECT userName FROM Users WHERE userName=?", (user,)) #Validar si exite en db
    data = c.fetchone()
    if data is None:
          print "User do not exist. Create one"
          databaseEngine.createUser(user)
          print "User created"
          c.execute("SELECT * FROM Users WHERE userName=?", (user,))
          userData = c.fetchone()
          print "\nWelcome " + userData[1] + "!!\n"

    else:
        c.execute("SELECT * FROM Users WHERE userName=?", (user,))
        userData = c.fetchone()
        print "\nWelcome " + userData[1] + "!!\n"
    
    control = input()
        
    if control == 1:
        databaseEngine.createMatchTable(userData)# Es un ejemplo
        print "Match created"

    elif control == 3:
        print "ok no"

    elif control == 6:
        print "Ok bye"

###Program Start##
if __name__ == "__main__":
    main()
