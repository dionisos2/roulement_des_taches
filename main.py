#!/bin/python

from taches_distributor import *

taches_list = Taches_list()
taches_list.load_xml("./taches.xml")

taches_distributor = Taches_distributor(taches_list)
print(taches_distributor.total_time())
print(taches_distributor.share_in(4))
