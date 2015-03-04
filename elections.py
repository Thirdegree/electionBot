import sqlite3
from datetime import date, datetime

conn = sqlite3.connect('elections.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

def get_election(subreddit):
    election = c.execute("SELECT * FROM elections WHERE subreddit=?", (subreddit,))
    return election.fetchone()

def get_upcomming_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY start")
    return [i for i in elections]

def get_ending_soon_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY end")
    return [i for i in elections]

def delete_election(subreddit):
    c.execute("DELETE FROM elections WHERE subreddit=?", (subreddit,))
    conn.commit()

def prune_elections():
    c.execute("DELETE FROM elections WHERE ?>end", (str(date.today()),))
    conn.commit()

def create_election(subreddit, url, start, end):
    c.execute("INSERT INTO elections VALUES (?, ?, ?, ?)", (subreddit, url, start, end))
    conn.commit()