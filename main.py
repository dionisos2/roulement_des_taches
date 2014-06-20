#!/bin/python

from taches_distributor import *

taches_list = Taches_list([])
taches_list.load_xml("./taches.xml")

taches_distributor = Taches_distributor(taches_list)
# print(taches_distributor.total_time())
distribution = taches_distributor.share_in(3, ["A", "B", "C"], ["P", "Q", "R"])
taches_distributor.share_with_one_more("uaei")

wiki = "= Tableau global ="
wiki += distribution.get_whole().wiki_table()
wiki += "= Tableaux de la semaine ="
for person in distribution.get_week():
    wiki += person.wiki_table()
wiki += "= Tableaux du mois ="
for person in distribution.get_month():
    wiki += person.wiki_table()

wiki_file = open("wiki_file", 'w', encoding='utf8')
wiki_file.write(wiki)

html = "<html>\n\
<head>\n\
<meta charset=\"UTF-8\" />\n\
<style type=\"text/css\">\n\
table { page-break-inside:auto }\n\
tr    { page-break-inside:avoid; page-break-after:auto }\n\
* {font-size:8px}\n\
</style>\n\
</head>\n\
<body>"
html += distribution.get_whole().html_table()
for person in distribution.get_week():
    html += person.html_table()
for person in distribution.get_month():
    html += person.html_table()
html += "</body>\n\
</html>"

html_file = open("html_file.html", 'w', encoding='utf8')
html_file.write(html)

distribution.get_whole().save_xml("xml_file.xml")
