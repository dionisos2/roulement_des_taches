from tache import Tache
import re
import xml
from xml.dom import minidom

class Taches_list:
    def __init__(self, list_of_taches, name = ""):
        self.list_of_taches = list_of_taches
        self.name = name

    def have(self, tache):
        for tache2 in self.list_of_taches:
            if(tache.numero == tache2.numero):
                return True
        return False

    def have_one_in(self, taches_list):
        assert(isinstance(taches_list, Taches_list))
        have = False
        for tache in taches_list:
            have = have or self.have(tache)
        return have

    def total_time(self, n=None):
        if(n == None):
            the_sum = sum((tache.get_time() for tache in self.list_of_taches))
        else:
            the_sum = sum((tache.get_time() for tache in filter(lambda tache: (tache.for_x_people >= n), self.list_of_taches)))
        return the_sum

    def append(self, tache):
        assert(isinstance(tache, Tache))
        self.list_of_taches.append(tache)

    def __iter__(self):
        for tache in self.list_of_taches:
            yield tache

    def get_tache_for_week(self):
        is_week = lambda tache:(tache.frequence[1] != "mois")
        return Taches_list(list(filter(is_week, self.list_of_taches)))

    def get_tache_for_month(self):
        is_week = lambda tache:(tache.frequence[1] == "mois")
        return Taches_list(list(filter(is_week, self.list_of_taches)))

    @classmethod
    def get_element(cls, tache_node, element):
        element_value = tache_node.getElementsByTagName(element)[0].firstChild.nodeValue
        if(element == "numero"):
            return int(element_value)
        elif(element == "nom"):
            return element_value
        elif(element == "temps"):
            return cls.str_to_temps(element_value)
        elif(element == "horaire"):
            return element_value
        elif(element == "frequence"):
            return cls.str_to_frequence(element_value)
        elif(element == "groupe"):
            return element_value
        else:
            raise ValueError("element should be in {numero, nom, temps, horaire, frequence, groupe} " + element + " given.")

    @classmethod
    def str_to_frequence(cls, frequence):
        cls.get_frequence = re.compile("(\d+)/(jour|semaine|mois)")
        tmp = cls.get_frequence.match(frequence)
        return (int(tmp.group(1)), tmp.group(2))

    @classmethod
    def str_to_temps(cls, temps):
        cls.get_min = re.compile("(\d+) min") # à sortir de la fonction pour optimiser
        cls.get_hour = re.compile("(\d+)h(\d+)")

        minute = cls.get_min.match(temps)
        hour = cls.get_hour.match(temps)

        if(minute):
            return int(minute.group(1))
        elif(hour):
            return int(hour.group(1))*60 + int(hour.group(2))
        else:
            raise ValueError("str_to_temps, unable to parse: " + temps)

    @classmethod
    def str_to_groups(cls, str_groups):
        cls.get_group = re.compile("(?:([^ +]*)(?: \+ )?)(.*)") #TOSEE pas top …

        group = cls.get_group.match(str_groups).groups()
        groups = [group[0]]
        while group[1] != "":
            str_groups = group[1]
            group = cls.get_group.match(str_groups).groups()
            groups.append(group[0])

        return groups

    def save_xml(self, xml_file):
        self.list_of_taches = sorted(self.list_of_taches, key=lambda tache:int(tache.numero))

        xml = "<?xml version=\"1.0\" ?>\n\
<taches>\n"

        for tache in self.list_of_taches:
            groups = self.str_to_groups(tache.attribution)
            for group in groups:
                tache_xml = "<tache>\n"
                tache_xml += "<numero>" + str(tache.numero) + "</numero>\n"
                tache_xml += "<nom>" + str(tache.nom) + "</nom>\n"
                tache_xml += "<temps>" + str(tache.temps) + " min</temps>\n"
                tache_xml += "<horaire>" + str(tache.horaire) + "</horaire>\n"
                tache_xml += "<frequence>" + str(tache.frequence[0])+"/"+ str(tache.frequence[1]) + "</frequence>\n"
                tache_xml += "<groupe>" + str(tache.groupe) + "</groupe>\n"
                if(not self.name):
                    tache_xml += "<attribution>" + str(group) + "</attribution>\n"
                tache_xml += "</tache>\n"
                xml += tache_xml

        xml += "</taches>"
        xml_file = open(xml_file, 'w', encoding='utf8')
        xml_file.write(xml)


    def load_xml(self, xml_file):
        doc = minidom.parse(xml_file)
        for tache in doc.documentElement.childNodes:
            if(tache.nodeType == minidom.Node.ELEMENT_NODE):
                numero = self.get_element(tache, "numero")
                nom = self.get_element(tache, "nom")
                temps = self.get_element(tache, "temps")
                horaire = self.get_element(tache, "horaire")
                frequence = self.get_element(tache, "frequence")
                groupe = self.get_element(tache, "groupe")
                self.list_of_taches.append(Tache(numero, nom, temps, horaire, frequence, groupe))

    def show_taches(self):
        print(str(self))

    def regroup_taches(self):
        regrouped_taches = {}
        i = 0
        for tache in self:
            if(tache.groupe == "*"):
                regrouped_taches[i] = Taches_list([tache])
                i += 1
            else:
                if(tache.groupe in regrouped_taches):
                    regrouped_taches[tache.groupe].append(tache)
                else:
                    regrouped_taches[tache.groupe] = Taches_list([tache])

        return regrouped_taches

    def __str__(self):
        tmp = ""
        for tache in self.list_of_taches:
            tmp += str(tache)
        return tmp


    def __getitem__(self, i):
        return self.list_of_taches[i]

    def __delitem__(self, i):
        del(self.list_of_taches[i])

    def __len__(self):
        return len(self.list_of_taches)

    def sort(self, key = None, reverse = False):
        self.list_of_taches = sorted(self.list_of_taches, reverse = reverse, key = key)


    def well_sort(self):
        if(self.name):
            self.list_of_taches.sort(reverse = True)
            # self.list_of_taches = sorted(self.list_of_taches, reverse=True, key=lambda tache:tache.frequence_by_day())
        else:
            self.list_of_taches = sorted(self.list_of_taches, reverse=False, key=lambda tache:tache.nom)

    def get_name(self):
        if(self.name):
            return self.name
        else:
            return "Activités"

    def html_table(self):
        self.well_sort()
        table = "<table border=\"1\">\n"
        table += "<caption><b>" + self.get_name() + "</b></caption>"
        table += "<tr>\n\
        <th>Effectif</th>\n\
        <th>Nom</th>\n\
        <th>Temps estimé</th>\n\
        <th>Horaire</th>\n\
        <th>Fréquence</th>"

        if(not self.name):
            table += "<th>Attribution</th>"

        table += "</tr>"

        for_x_people = self.list_of_taches[0].for_x_people
        rowspan = [0]

        for tache in self.list_of_taches:
            if(for_x_people != tache.for_x_people):
                rowspan.append(1)
                for_x_people = tache.for_x_people
            else:
                rowspan[-1] += 1

        current_rowspan = 0
        count = 0
        for tache in self.list_of_taches:
            table += "<tr>\n"
            if(count == 0):
                table += "<td rowspan=\""+ str(rowspan[current_rowspan]) +"\">" + str(tache.for_x_people) + "</td>\n"
                count = rowspan[current_rowspan] - 1
                current_rowspan += 1
            else:
                count -= 1
            table += "<td>" + str(tache.nom) + "</td>\n"
            table += "<td>" + str(tache.temps) + " min</td>\n"
            table += "<td>" + str(tache.horaire) + "</td>\n"
            table += "<td>" + str(tache.frequence[0]) + "/" + str(tache.frequence[1]) + "</td>\n"
            if(not self.name):
                table += "<td>" + str(tache.attribution) + "<td>\n"
            table += "</tr>\n"
        table += "</table>\n"

        return table

    def wiki_table(self):
        self.well_sort()

        table = "{| border=\"1\" style=\"width:500px;\"\n"
        table += "|+'''" + self.get_name() + "'''\n"
        table += "\
!Nom\n\
!Temps estimé\n\
!Horaire\n\
!Fréquence\n"

        if(not self.name):
            table += "!Attribution\n"

        for tache in self.list_of_taches:
            table += "|-\n"
            table += "|" + str(tache.nom) + "\n"
            table += "|" + str(tache.temps) + " min\n"
            table += "|" + str(tache.horaire) + "\n"
            table += "|" + str(tache.frequence[0])+"/"+ str(tache.frequence[1]) + "\n"
            if(not self.name):
                table += "|" + str(tache.attribution) + "\n"

        table += "|}"
        return table

