from taches_list import *

class Taches_distributor:
    def __init__(self, taches_list):
        assert(isinstance(taches_list, Taches_list))
        self.taches_list = taches_list

    def share_in(self, n, week_names, month_names):
        result = {"week": self._share_in_(self.taches_list.get_tache_for_week(), n, week_names),
                  "month": self._share_in_(self.taches_list.get_tache_for_month(), n, month_names)}
        result["global"] = self.global_distribution(result)
        return result

    def global_distribution(self, distribution):
        for tache in self.taches_list:
            for person in (distribution["week"] + distribution["month"]):
                if(tache in person):
                    tache.attribution = person.name
                    break
        return self.taches_list

    def _share_in_(self, taches_list, n, names):

        time_by_person = taches_list.total_time() / n
        regrouped_taches_list = taches_list.regroup_taches()
        people = []
        for i in range(n):
            people.append(Taches_list([], names[i]))

        for (tmp, regrouped_taches) in sorted(regrouped_taches_list.items(), reverse = True, key = lambda keyvalue: keyvalue[1].total_time()):
            sorted_people = sorted(people, key=lambda person: person.total_time())

            ok = False
            for person in sorted_people:
                if not(person.have_one_in(regrouped_taches)):
                    for tache in regrouped_taches:
                        person.append(tache)
                    ok = True
                    break

            if(not ok):
                raise ValueError("impossible de répartir convenablement")

        return people

    def total_time(self):
        return self.taches_list.total_time()

    def show_regrouped_taches_list(self, regrouped_taches_list):
        for (group, regrouped_taches_list) in regrouped_taches_list.items():
            print("#"*20+str(group)+"#"*20)
            print(regrouped_taches)
            print("#"*20+str(group)+"#"*20)
