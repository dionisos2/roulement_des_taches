#!/bin/python

from taches_distributor import *

taches_list = Taches_list([])
taches_list.load_xml("./taches.xml")

taches_distributor = Taches_distributor(taches_list)
# print(taches_distributor.total_time())
distribution = taches_distributor.share_in(4, ["A", "B", "C", "D"], ["P", "Q", "R", "S"])

print("= Tableau global =")
print(distribution["global"].wiki_table())
print("= Tableaux de la semaine =")
for person in distribution["week"]:
    print(person.wiki_table())
print("= Tableaux du mois =")
for person in distribution["month"]:
    print(person.wiki_table())


print("<html>\n\
<head>\n\
<meta charset=\"UTF-8\" />\n\
<style type=\"text/css\">\n\
table { page-break-inside:auto }\n\
tr    { page-break-inside:avoid; page-break-after:auto }\n\
</style>\n\
</head>\n\
<body>")
print(distribution["global"].html_table())
for person in distribution["week"]:
    print(person.html_table())
for person in distribution["month"]:
    print(person.html_table())
print("</body>\n\
</html>")
