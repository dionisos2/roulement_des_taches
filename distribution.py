from taches_list import *
from mylib.checking import *

class Distribution:
    def __init__(self):
        self.whole = None
        self.week = None
        self.month = None

    def set_whole(self, whole):
        assert(isinstance(whole, Taches_list))
        self.whole = whole

    def set_week(self, week):
        assert(is_all_instance(week, Taches_list))
        self.week = week

    def set_month(self, month):
        assert(is_all_instance(month, Taches_list))
        self.month = month

    def get_whole(self):
        return self.whole

    def get_week(self):
        return self.week

    def get_month(self):
        return self.month

    def __str__(self):
        if(self.whole != None):
            return str(self.whole)
        else:
            return "Non initialisé"
