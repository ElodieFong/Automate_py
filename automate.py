import re
class AUTO():
    def __init__(self):
        self.alphabet = 0
        self.etats = 0
        self.entrees = 0
        self.sorties = 0
        self.transitions = 0

    def display(self):
        # affichage temporaire
        print("l'aphabet de l'automate est: ", self.alphabet)
        print("les états de l'automate sont: ", self.etats)
        print("les entrées de l'automate sont: ", self.entrees)
        print("les sorties de l'automate sont: ", self.sorties)
        print("la tables des états est: ")
        for keys, values in self.transitions.items():
            print(keys, values)

    def insert(self, file):
        with open(file, 'r') as f:
            lignes = [ligne.strip() for ligne in f if ligne.strip()]
        nb_lettre = int(lignes[0])
        alphabet = [chr(ord('a') + i) for i in range(nb_lettre)]
        nb_etats = int(lignes[1])
        etats = list(range(nb_etats))
        ent_info = list(map(int, lignes[2].split()))
        entrees = list(ent_info[1:])
        sor_info = list(map(int, lignes[3].split()))
        sorties = list(sor_info[1:])
        nb_trans = int(lignes[4])
        transi = {etat: {} for etat in etats}
        for ligne in lignes[5:5 + nb_trans]:
            match = re.match(r"(\d+)([a-zA-Z]+)(\d+)", ligne)
            depart, symbole, arrivee = int(match.group(1)), match.group(2), int(match.group(3))
            if symbole not in transi[depart]:
                transi[depart][symbole] = set()
            transi[depart][symbole].add(arrivee)
        self.alphabet = alphabet
        self.etats = etats
        self.entrees = entrees
        self.sorties = sorties
        self.transitions = transi

    def estDeter(self):
        if len(self.entrees) == 1:
            for etat in self.transitions.values():
                for transi in etat.values():
                    if len(transi) > 1:
                        return False
        return True

    def estStand(self):
        if len(self.entrees) != 1:
            return False
        for etat in self.transitions.values():
            for transi in etat.values():
                for i in transi:
                    if i == 0:
                        return False
        return True

    def estComp(self):
        if sum(map(len, self.transitions.values())) == len(self.alphabet)*len(self.etats):
            return True
        return False

    def standardisation(self):
        if self.estStand() == True:
            print("L'automate est déjà standard")
        else:
            i_sortie = False
            self.etats.append('i')
            self.transitions.update({'i': {}})
            for i in self.entrees:
                for symbole, destinations in self.transitions.get(i, {}).items():
                    if symbole not in self.transitions['i']:
                        self.transitions['i'][symbole] = set()
                    self.transitions['i'][symbole].update(destinations)
                if i in self.sorties:
                    self.sorties.remove(i)
                    i_sortie = True
            if i_sortie == True:
                self.sorties.append('i')
            self.entrees = ['i']
            print("Voici l'automate standardisé")
            self.display()