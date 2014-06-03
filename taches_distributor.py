from taches_list import *

class Taches_distributor:
    def __init__(self, taches_list):
        assert(isinstance(taches_list, Taches_list))
        self.taches_list = taches_list

    def share_in(self, n):
        return {"week": self._share_in_(self.taches_list.get_tache_for_week(), n),
                "month": self._share_in_(self.taches_list.get_tache_for_month(), n)}

    def _share_in_(self, taches_list, n):
        time_by_person = taches_list.total_time() / n

    def total_time(self):
        return self.taches_list.total_time()

    def show_regrouped_taches(self, regrouped_taches):
        for (group, regrouped_taches) in regrouped_taches.items():
            print("#"*20+str(group)+"#"*20)
            print(regrouped_taches)
            print("#"*20+str(group)+"#"*20)
