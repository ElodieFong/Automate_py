import re
class AUTO():
    def __init__(self):
        self.alphabet = [] #liste qui contient les lettres de l'alphabet
        self.etats = [] #liste des états de l'automate
        self.entrees = [] #liste des états entrées
        self.sorties = [] #liste des états sorties
        self.transitions = {} #dico { états : { lettres : [états transitoires/arrivées] } }

    def display(self):
        # affichage temporaire
        print("l'aphabet de l'automate est: ", self.alphabet)
        print("les états de l'automate sont: ", self.etats)
        print("les entrées de l'automate sont: ", self.entrees)
        print("les sorties de l'automate sont: ", self.sorties)
        print("la tables des transitions est: ")
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
                transi[depart][symbole] = list()
            transi[depart][symbole].append(arrivee)
        self.alphabet = alphabet
        self.etats = etats
        self.entrees = entrees
        self.sorties = sorties
        self.transitions = transi

    def estDeter(self):
        if len(self.entrees) != 1:
            return False
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
            for etat in self.entrees:
                # récupère les lettres et les états arrivées de l'état[i] dans la liste des entrées
                for lettre, arrivee in self.transitions.get(etat, {}).items():
                    if lettre not in self.transitions['i']:
                        #ajoute les valeurs de l'état[i]: lettres et états d'arrivées
                        self.transitions['i'][lettre] = arrivee
                if etat in self.sorties:
                    self.sorties.remove(etat)
                    #il existe un état entrée sortie donc i est une sortie
                    i_sortie = True
            if i_sortie == True:
                self.sorties.append('i')
            self.entrees = ['i']
            print("Voici l'automate standardisé")
            self.display()

    def completion(self): #temp
        if self.estComp() == True:
            return print("L'automate est déjà complet")
        self.etats.append('P')
        self.transitions['P'] = {symbole: ['P'] for symbole in self.alphabet}
        for etat in self.etats:
            for symbole in self.alphabet:
                if symbole not in self.transitions.get(etat, {}):
                    self.transitions[etat][symbole] = ['P']
        print("L'automate a été complété.")
        self.display()

    def determinisation(self): #temp
        if self.estDeter() == True and self.estComp() == True:
            print("L'automate est déjà déterministe et complet")

    def minimisation(self): #temp
        if self.estDeter() == False or self.estComp() == False:
            self.determinisation()

    def complementaire(self):
        new_sorties = [etat for etat in self.etats if etat not in self.sorties]
        self.sorties = new_sorties
        print("Voici l'automate complémentaire")
        self.display()