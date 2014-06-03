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

    def __str__(self):
        tmp = "-"*10 + "tache" + "-"*10 + "\n"
        tmp += "numero: " + str(self.numero) + "\n"
        tmp += "nom: " + str(self.nom) + "\n"
        tmp += "temps: " + str(self.temps) + "\n"
        tmp += "horaire: " + str(self.horaire) + "\n"
        tmp += "frequence: " + str(self.frequence[0])+ "/" + str(self.frequence[1]) + "\n"
        tmp += "groupe: " + str(self.groupe) + "\n"
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
