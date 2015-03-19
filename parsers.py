import re
import praw
from datetime import date

class WikiParser():
    def __init__(self, r, subreddit=None):
        self.r = r
        if subreddit:
            self.raw_conditions = get_raw_conditions(subreddit)
        else:
            self.raw_conditions = ""

    def get_raw_conditions(self, subreddit):
        page = self.r.get_wiki_page(subreddit, "election")
        self.raw_conditions = page.content_md

    def get_frequency(self):
        pattern = r"(?i)Frequency: (\d+) days"
        match = re.search(pattern, self.raw_conditions)
        freq = 0
        if match:
            freq = int(match.group(1))
        return freq

    def get_next_election(self):
        pattern = r"(?i)First Election: (\d+-\d+-\d+)"
        date = ""
        match = re.search(pattern, self.raw_conditions)
        if match:
            date = match.group(1)
        return date

    def get_duration(self):
        pattern = r"(?i)Election Duration: (\d+) days"
        match = re.search(pattern, self.raw_conditions)
        duration = 0
        if match:
            duration = int(match.group(1))
        return duration

    def get_positions(self):
        pattern = r"(?i)Mod Positions Available: (\d+)"
        match = re.search(pattern, self.raw_conditions)
        positions = 0
        if match:
            positions = int(match.group(1))
        return positions