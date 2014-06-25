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
        distribution.create_whole()
        return distribution

    def share_with_one_less(self, distribution):
        assert(isinstance(distribution, Distribution))
        distribution = copy.copy(distribution)
        distribution.set_week(self._share_with_one_less_(distribution.get_week()))
        distribution.set_month(self._share_with_one_less_(distribution.get_month()))
        distribution.create_whole()

        return distribution

    def _share_with_one_less_(self, people):
        time_by_person = sum((person.total_time() for person in people))
        # regrouped_taches_list = taches_list.regroup_taches()
        # people = []
        # for i in range(n):
        #     people.append(Taches_list([], names[i]))

        # for (tmp, regrouped_taches) in sorted(regrouped_taches_list.items(), reverse = True, key = lambda keyvalue: keyvalue[1].total_time()):
        #     sorted_people = sorted(people, key=lambda person: person.total_time())

        #     ok = False
        #     for person in sorted_people:
        #         if not(person.have_one_in(regrouped_taches)):
        #             for tache in regrouped_taches:
        #                 person.append(tache)
        #             ok = True
        #             break

        #     if(not ok):
        #         raise ValueError("impossible de répartir convenablement")
        # if(not self.is_valid(people)):
        #     raise ValueError("Il y a une trop grande différence de temps dans la répartition, temps moyen:" + str(time_by_person) + " temps trouvé:" + str(person.total_time()))

        return people

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
