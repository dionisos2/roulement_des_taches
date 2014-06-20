from taches_list import *
from distribution import Distribution
import copy

class Taches_distributor:
    def __init__(self, taches_list, max_diff = 0.05):
        assert(isinstance(taches_list, Taches_list))
        self.taches_list = taches_list
        self.max_diff = max_diff #différence max de temps d’activité entre les personnes(pas tout à fait exacte)

    def share_in(self, n, week_names, month_names):
        distribution = Distribution()
        distribution.set_week(self._share_in_(self.taches_list.get_tache_for_week(), n, week_names))
        distribution.set_month(self._share_in_(self.taches_list.get_tache_for_month(), n, month_names))
        distribution.set_whole(self.global_distribution(distribution))
        return distribution

    def share_with_one_more(self, distribution):
        assert(isinstance(distribution, Distribution))
        

    def global_distribution(self, distribution):
        taches_list = copy.copy(self.taches_list)
        for tache in taches_list:
            for person in (distribution.get_week() + distribution.get_month()):
                if(tache in person):
                    tache.attribution = person.name
                    break

        taches_list.sort(reverse=False, key=lambda tache:tache.numero)

        i = 1
        while (i < len(taches_list)):
            if(taches_list[i-1].numero == taches_list[i].numero):
                taches_list[i-1].attribution += " + " + taches_list[i].attribution
                del(taches_list[i])
            else:
                i += 1
        return taches_list

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
        for person in people:
            print(person.total_time())
            if((person.total_time() - time_by_person)/time_by_person > self.max_diff):
                raise ValueError("Il y a une trop grande différence de temps dans la répartition, temps moyen:" + str(time_by_person) + " temps trouvé:" + str(person.total_time()))

        return people

    def total_time(self):
        return self.taches_list.total_time()

    def show_regrouped_taches_list(self, regrouped_taches_list):
        for (group, regrouped_taches_list) in regrouped_taches_list.items():
            print("#"*20+str(group)+"#"*20)
            print(regrouped_taches)
            print("#"*20+str(group)+"#"*20)
