import sqlite3

conn = sqlite3.connect('settings.db')
c = conn.cursor()


#get_settings :: String -> (String, String, Int, Int, Int)
def get_settings(subreddit):
    settings = c.execute("SELECT * FROM settings WHERE subreddit=?", (subreddit,))
    return settings.fetchone()

def change_settings(subreddit, first, frequency, duration, positions):
    c.execute("UPDATE settings SET first=?, frequency=?, duration=?, positions=? WHERE subreddit=?", (first, frequency, duration, positions, subreddit))
    conn.commit()

def delete_subreddit(subreddit):
    c.execute("DELETE FROM settings WHERE subreddit=?", (subreddit,))
    conn.commit()

def get_all_settings():
    settings = c.execute("SELECT * FROM settings ORDER BY subreddit")
    return [i for i in settings]

def add_subreddit(subreddit, first, frequency, duration, positions):
    c.execute("INSERT INTO settings VALUES (?, ?, ?, ?, ?)", (subreddit, first, frequency, duration, positions))
    conn.commit()