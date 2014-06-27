import xml
from xml.dom import minidom

class Tache:
    def __init__(self, numero, nom, temps, horaire, frequence, groupe):
        self.numero = numero
        self.nom = nom
        self.temps = temps
        self.horaire = horaire
        self.frequence = frequence
        self.groupe = groupe
        self.attribution = None
        self.for_x_people = None

    def __str__(self):
        tmp = "-"*10 + "tache" + "-"*10 + "\n"
        tmp += "numero: " + str(self.numero) + "\n"
        tmp += "nom: " + str(self.nom) + "\n"
        tmp += "temps: " + str(self.temps) + "\n"
        tmp += "horaire: " + str(self.horaire) + "\n"
        tmp += "frequence: " + str(self.frequence[0])+ "/" + str(self.frequence[1]) + "\n"
        tmp += "groupe: " + str(self.groupe) + "\n"
        tmp += "attribution: " + str(self.attribution) + "\n"
        return tmp

    def frequence_by_day(self):
        if(self.frequence[1] == "mois"):
            day = 30
        elif(self.frequence[1] == "semaine"):
            day = 7
        elif(self.frequence[1] == "jour"):
            day = 1
        return self.frequence[0] / day

    def get_time(self):
        return self.temps * self.frequence_by_day()

    def __lt__(self, other):
        return (self.for_x_people < other.for_x_people) or ((self.for_x_people == self.for_x_people) and (self.frequence_by_day() < other.frequence_by_day()))

    def __eq__(self, other):
        eq = (self.numero == other.numero)
        eq &= (self.nom == other.nom)
        eq &= (self.temps == other.temps)
        eq &= (self.horaire == other.horaire)
        eq &= (self.frequence == other.frequence)
        eq &= (self.groupe == other.groupe)
        return eq
