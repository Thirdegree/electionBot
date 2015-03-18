import regex
import praw
from datetime import date

class WikiParser(Object):
    def __init__(self, r):
        self.r = r
        self.raw_conditions = ""

    def get_raw_conditions(subreddit):
        page = self.r.get_wiki_page(subreddit, "election")
        self.raw_conditions = page.content_md

    def get_frequency():
        pattern = r"(?i)Frequency: (\d+) days"
        match = re.match(pattern, self.raw_conditions)
        freq = 0
        if match:
            freq = int(match.group(1))
        return freq

    def get_next_election():
        pattern = r"(?i)First election: (\d+-\d+-\d+)"
        date = ""
        match = re.match(pattern, self.raw_conditions)
        if match:
            date = match.group(1)
        return date

    def get_duration():
        pattern = r"(?i)Election Duration: (\d+) days"
        match = re.match(pattern, self.raw_conditions)
        duration = 0
        if match:
            duration = int(match.group(1))
        return duration

    def get_positions():
        pattern = r"(?i)Mod Positions Available: (\d+)"
        match = re.match(pattern, self.raw_conditions)
        positions = 0
        if match:
            positions = int(match.group(1))
        return positions