import json

modlistFile = open('modlist.json', 'r+')
modlist = json.loads(modlistFile.read())

def add_subreddit(subreddit):
    modlist[subreddit] = {'numberOfMods':0, 'mods':[]}
    modlistFile.seek(0)
    modlistFile.truncate()
    modlistFile.write(json.dumps(modlist))

def delete_subreddit(subreddit):
    del modlist[subreddit]
    modlistFile.seek(0)
    modlistFile.truncate()
    modlistFile.write(json.dumps(modlist))

def get_subreddit(subreddit):
    return modlist[subreddit]