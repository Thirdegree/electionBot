import json

modlistFile = open('modlist.json', 'r+')
modlist = json.loads(modlistFile.read())

def add_subreddit(subreddit, mods, nominatedMods = [],numberOfMods=1):
    modlist[subreddit] = {'numberOfMods':numberOfMods, 'mods':mods, 'nominatedMods':nominatedMods}
    print modlist
    modlistFile.seek(0)
    modlistFile.truncate()
    modlistFile.write(json.dumps(modlist, indent=4))
    modlistFile.seek(0)

def delete_subreddit(subreddit):
    del modlist[subreddit]
    modlistFile.seek(0)
    modlistFile.truncate()
    modlistFile.write(json.dumps(modlist, indent=4))
    modlistFile.seek(0)

def get_subreddit(subreddit):
    return modlist[subreddit]

def mod_nominated(subreddit, nominated):
    modlist[subreddit]['nominatedMods'] = nominated
    modlistFile.seek(0)
    modlistFile.truncate()
    modlistFile.write(json.dumps(modlist, indent=4))
    modlistFile.seek(0)