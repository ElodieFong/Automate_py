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
            depart, symbole, arrivee = int(ligne[0]), ligne[1], int(ligne[2])
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
                        return print("L'automate n'est pas déterministe")
        return print("L'automate est déterministe")

    def estStand(self):
        if len(self.entrees) != 1:
            return print("L'automate n'est standard")
        for etat in self.transitions.values():
            for transi in etat.values():
                for i in transi:
                    if i == 0:
                        return print("L'automate n'est standard")
        return print("L'automate est standard")

    def estComp(self):
        if sum(map(len, self.transitions.values())) == len(self.alphabet)*len(self.etats):
            print("L'automate est complet")
        print("L'automate n'est pas complet")

