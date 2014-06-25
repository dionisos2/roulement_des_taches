from taches_list import *
from mylib.checking import *
import copy

class Distribution:
    def __init__(self):
        self.whole = None
        self.week = None
        self.month = None
        self.whole_without_duplicate = None

    def create_whole(self):
        self.whole = Taches_list([])
        for person in (self.week + self.month):
            for tache in person:
                tache.attribution = person.name
                self.whole.append(tache)

        self.whole.sort(reverse=False, key=lambda tache:tache.numero)
        self.create_whole_without_duplicate()

    def create_whole_without_duplicate(self):
        self.whole_without_duplicate = copy.deepcopy(self.whole)
        whole = self.whole_without_duplicate

        i = 1
        while (i < len(whole)):
            if(whole[i-1].numero == whole[i].numero):
                whole[i-1].attribution += " + " + whole[i].attribution
                del(whole[i])
            else:
                i += 1

    def set_whole_without_duplicate(self, whole_without_duplicate):
        assert(isinstance(whole_without_duplicate, Taches_list))
        self.whole_without_duplicate = whole_without_duplicate

    def get_whole_without_duplicate(self):
        return self.whole_without_duplicate

    def set_whole(self, whole):
        assert(isinstance(whole, Taches_list))
        self.whole = whole

    def get_whole(self):
        return self.whole

    def set_week(self, week):
        assert(is_all_instance(week, Taches_list))
        self.week = week

    def get_week(self):
        return self.week

    def set_month(self, month):
        assert(is_all_instance(month, Taches_list))
        self.month = month

    def get_month(self):
        return self.month

    def __str__(self):
        if(self.whole != None):
            return str(self.whole)
        else:
            return "Non initialisé"
