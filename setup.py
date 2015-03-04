import sqlite3
import json

conn_set = sqlite3.connect("settings.db")
c_set = conn_set.cursor()
c_set.execute('''CREATE TABLE IF NOT EXISTS settings 
                (subreddit text, first text, frequency integer, duration integer, positions integer)''')
conn_set.commit()
conn_set.close()
#-------------------

with open('modlist.json', 'w+') as modlist:
    modlist.write(json.dumps({"_structure":"subreddit:{'numberOfMods':0, 'mods':[]}"}, 
                                indent=4))

#-------------------
conn_elect = sqlite3.connect('elections.db')
c_elect = conn_elect.cursor()
c_elect.execute('''CREATE TABLE IF NOT EXISTS elections
                    (subreddit text, url text, nominationStart text, electionStart text, electionEnd text)''')
conn_elect.commit()
conn_elect.close()

#-------------------
with open('logins.json', 'w+') as logins:
    username = raw_input("Bot username: ")
    password = raw_input("Bot password: ")
    clientId = raw_input("Client ID: ")
    clientSecret = raw_input("Client Secret: ")
    logins.write(json.dumps({
                            "username":username,
                            "password":password,
                            "clientId":clientId,
                            "clientSecret":clientSecret
                            }, 
                            indent=4))