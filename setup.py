import sqlite3
import json
import os.path

#------------------ DataBase for holding potential alterations in settings. Defaults are 
#------------------    text      date  days  days   position
#------------------ (subreddit,  first, 28,   7,     1)
conn_set = sqlite3.connect("settings.db")
c_set = conn_set.cursor()
c_set.execute('''CREATE TABLE IF NOT EXISTS settings 
                (subreddit text, next_ele text, frequency integer, duration integer, positions integer)''')
conn_set.commit()
conn_set.close()

#------------------- JSON file (easier to hand modify) Defaults are 
#------------------- 'subreddit': {'numberOfMods':1, 'mods':[modName], 'nominatedMods':[]}
if not os.path.isFile("modlist.json"):
    with open('modlist.json', 'w+') as modlist:
        modlist.write(json.dumps({"_structure":"subreddit:{'numberOfMods':0, 'mods':[], 'nominatedMods':[]}"}, 
                                indent=4))

#------------------- DB again for holding all possible elections.
#------------------- no need for defaults because there's nothing that could have a defualt
conn_elect = sqlite3.connect('elections.db')
c_elect = conn_elect.cursor()
c_elect.execute('''CREATE TABLE IF NOT EXISTS elections
                    (subreddit text, nominationUrl text, electionUrl text, nominationStart text, electionStart text, electionEnd text)''')
conn_elect.commit()
conn_elect.close()

#------------------- Secrets are ment to be kept secret. 
#-------------------
if not os.path.isfile('logins.json'):
    with open('logins.json', 'w+') as logins:
        username = raw_input("Bot username: ")
        password = raw_input("Bot password: ")
        clientId = raw_input("Client ID: ")
        clientSecret = raw_input("Client Secret: ")
        logins.write(json.dumps({
                                "username":username,
                                "password":password,
                                "clientId":clientId,
                                "clientSecret":clientSecret,
                                "accessToken":""
                                }, 
                                indent=4))