#!/bin/python

from taches_distributor import *

taches_list = Taches_list([])
taches_list.load_xml("./taches.xml")

taches_distributor = Taches_distributor(taches_list)
# print(taches_distributor.total_time())
distribution = taches_distributor.share_in(4, ["A", "B", "C", "D"], ["A*", "B*", "C*", "D*"])

print(distribution["global"].wiki_table())

for person in distribution["week"]:
    print(person.wiki_table())

for person in distribution["month"]:
    print(person.wiki_table())
