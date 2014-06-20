from taches_list import *

class Distribution:
    def __init__(self):
        self.whole = []
        self.week = []
        self.month = []

    def set_whole(self, whole):
        self.whole = whole

    def set_week(self, week):
        self.week = week

    def set_month(self, month):
        self.month = month

    def get_whole(self):
        return self.whole

    def get_week(self):
        return self.week

    def get_month(self):
        return self.month
