import sqlite3

conn = sqlite3.connect('settings.db')
c = conn.cursor()

class Settings():
    def __init__(self, subreddit, next_ele, frequency, duration, positions):
        self.subreddit = subreddit
        self.next_ele = next_ele
        self.frequency = frequency
        self.duration = duration
        self.positions = positions

    def __str__(self):
        return self.subreddit + " Settings"

    __repr__ = __str__



#get_settings :: String -> (String, String, Int, Int, Int)
def get_settings(subreddit):
    settings = c.execute("SELECT * FROM settings WHERE subreddit=?", (subreddit,))
    sett = settings.fetchone()
    if sett:
        return Settings(*sett)
    return None

def change_settings(subreddit, next_ele, frequency, duration, positions):
    c.execute("UPDATE settings SET next_ele=?, frequency=?, duration=?, positions=? WHERE subreddit=?", (next_ele, frequency, duration, positions, subreddit))
    conn.commit()

def delete_subreddit(subreddit):
    c.execute("DELETE FROM settings WHERE subreddit=?", (subreddit,))
    conn.commit()

def get_all_settings():
    settings = c.execute("SELECT * FROM settings ORDER BY subreddit")
    return [Settings(*i) for i in settings]

def add_subreddit(subreddit, next_ele, frequency, duration, positions):
    c.execute("INSERT INTO settings VALUES (?, ?, ?, ?, ?)", (subreddit, next_ele, frequency, duration, positions))
    conn.commit()