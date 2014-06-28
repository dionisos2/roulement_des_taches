#!/bin/python

from taches_distributor import *

taches_list = Taches_list([])
taches_list.load_xml("./taches.xml")

taches_distributor = Taches_distributor(taches_list)

distribution = taches_distributor.share_up_to(5, ["A", "B", "C","D", "E"], ["P", "Q", "R", "S", "T"])

for i in range(2,6):
    print("-"*10 + str(i) + "-"*10)
    for key in range(i):
        print(distribution.get_week()[key].total_time(i))

# wiki = "= Tableau global ="
# wiki += distribution.get_whole_without_duplicate().wiki_table()

wiki = "= Tableaux de la semaine ="
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
table { page-break-inside:avoid }\n\
tr    { page-break-inside:avoid; page-break-after:auto }\n\
* {font-size:15px}\n\
</style>\n\
</head>\n\
<body>"
# html += distribution.get_whole_without_duplicate().html_table()
for person in distribution.get_week():
    html += person.html_table()
for person in distribution.get_month():
    html += person.html_table()
html += "</body>\n\
</html>"

html_file = open("html_file.html", 'w', encoding='utf8')
html_file.write(html)

distribution.get_whole().save_xml("xml_file.xml")
