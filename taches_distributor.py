from taches_list import *
from distribution import Distribution
import copy
import random

class Taches_distributor:
    def __init__(self, taches_list, max_diff = 0.15):
        assert(isinstance(taches_list, Taches_list))
        self.taches_list = taches_list
        self.max_diff = max_diff #différence max de temps d’activité entre les personnes(pas tout à fait exacte)

    def share_up_to(self, n, week_names, month_names):
        distribution = self.share_in(n, week_names, month_names)

        decremented_distribution = copy.deepcopy(distribution)
        for i in range(n-2):
            decremented_distribution = self.share_with_one_less(decremented_distribution)
            self._spread_taches_(distribution.get_week(), decremented_distribution.get_week())
            self._spread_taches_(distribution.get_month(), decremented_distribution.get_month())

        return distribution

    def _spread_taches_(self, people, decremented_people):
        for (key, person) in enumerate(decremented_people):
            for tache in person:
                if not(next((tache2 for tache2 in people[key] if tache2 == tache), None)):
                    tache.for_x_people = len(decremented_people)
                    people[key].append(tache)

    def share_in(self, n, week_names, month_names):
        distribution = Distribution()
        distribution.set_week(self._share_in_(self.taches_list.get_tache_for_week(), n, week_names))
        distribution.set_month(self._share_in_(self.taches_list.get_tache_for_month(), n, month_names))
        distribution.create_whole()
        return distribution


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
                        tache.for_x_people = n
                        person.append(tache)
                    ok = True
                    break

            if(not ok):
                raise ValueError("impossible de répartir convenablement")
        if(not self.is_valid(people)):
            raise ValueError("Il y a une trop grande différence de temps dans la répartition, temps moyen:" + str(time_by_person) + " temps trouvé:" + str(person.total_time()))

        return people

    def share_with_one_less(self, distribution):
        assert(isinstance(distribution, Distribution))
        distribution = copy.deepcopy(distribution)
        distribution.set_week(self._share_with_one_less_(distribution.get_week()))
        distribution.set_month(self._share_with_one_less_(distribution.get_month()))
        distribution.create_whole()

        return distribution

    def _share_with_one_less_(self, people):
        time_by_person = sum((person.total_time() for person in people))/(len(people) -1)

        taches_list = people[-1]
        regrouped_taches_list = taches_list.regroup_taches()
        del people[-1]

        for (tmp, regrouped_taches) in sorted(regrouped_taches_list.items(), reverse = True, key = lambda keyvalue: keyvalue[1].total_time()):
            sorted_people = sorted(people, key=lambda person: person.total_time())

            ok = False
            for person in sorted_people:
                if not(person.have_one_in(regrouped_taches)):
                    for tache in regrouped_taches:
                        tache.for_x_people = len(people)
                        person.append(tache)
                    ok = True
                    break

            if(not ok):
                raise ValueError("impossible de répartir convenablement")
        if(not self.is_valid(people)):
            raise ValueError("Il y a une trop grande différence de temps dans la répartition, temps moyen:" + str(time_by_person) + " temps trouvé:" + str(person.total_time()))

        return people

    def is_valid(self, people):
        n = len(people)
        sum_time = sum((person.total_time() for person in people))
        time_by_person = sum_time / n

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
