from taches_list import *
from distribution import Distribution
import copy
import random

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

    def share_with_one_more(self, distribution, name):
        assert(isinstance(distribution, Distribution))

        for i in range(1000):
            current_distribution = self.share_with_one_more_uncertain(distribution, name)
            if self.is_valid(current_distribution.get_week()):
                return current_distribution
            else:
                current_distribution = self.share_with_one_more_uncertain(distribution, name)

        raise ValueError("Arf, raté")

    def share_with_one_more_uncertain(self, distribution, name):
        assert(isinstance(distribution, Distribution))
        distribution = copy.copy(distribution)

        people = distribution.get_week()
        people.append(Taches_list([], name))

        while(min(people, key = lambda person:person.total_time()) == people[-1]):
            disadvantaged_person = max(people, key=lambda person: person.total_time())
            key = random.randint(0, len(disadvantaged_person)-1)
            tache = disadvantaged_person[key]
            tache.attribution = name
            people[-1].append(tache)
            del disadvantaged_person[key]

        return distribution


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
        if(not self.is_valid(people)):
            raise ValueError("Il y a une trop grande différence de temps dans la répartition, temps moyen:" + str(time_by_person) + " temps trouvé:" + str(person.total_time()))

        return people

    def is_valid(self, people):
        sum_time = sum((person.total_time() for person in people))
        time_by_person = sum_time / len(people)

        for person in people:
            if((person.total_time() - time_by_person)/time_by_person > self.max_diff):
                return False
        return True

    def total_time(self):
        return self.taches_list.total_time()

    def show_regrouped_taches_list(self, regrouped_taches_list):
        for (group, regrouped_taches_list) in regrouped_taches_list.items():
            print("#"*20+str(group)+"#"*20)
            print(regrouped_taches)
            print("#"*20+str(group)+"#"*20)
