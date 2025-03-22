import re
class AUTO():
    def __init__(self):
        self.alphabet = [] #liste qui contient les lettres de l'alphabet
        self.etats = [] #liste des états de l'automate
        self.entrees = [] #liste des états entrées
        self.sorties = [] #liste des états sorties
        self.transitions = {} #dico { états : { lettres : [états transitoires/arrivées] } }

    def insert(self, myfile):
        with open(myfile, 'r') as f:
            lignes = [ligne.strip() for ligne in f if ligne.strip()]

        nb_symb = int(lignes[0])
        alphabet = {chr(ord('a') + i) for i in range(nb_symb)}

        # Mapping pour transformer noms d'états (ex: 'P') en entiers
        etat_map = {}
        etat_counter = 0
        def get_etat_id(name):
            nonlocal etat_counter
            if name not in etat_map:
                if name == 'P':
                    etat_map[name] = 'P'
                else:
                    etat_map[name] = etat_counter
                    etat_counter += 1
            return etat_map[name]
        # États initiaux
        ent_info = lignes[2].split()
        entrees = {get_etat_id(s) for s in ent_info[1:]}
        # États finaux
        sor_info = lignes[3].split()
        sorties = {get_etat_id(s) for s in sor_info[1:]}

        nb_trans = int(lignes[4])
        transi = {}
        etats = set()

        for i in range(5, 5 + nb_trans):
            ligne = lignes[i].strip()
            match = re.match(r"([a-zA-Z0-9]+)([a-zA-Z]+)([a-zA-Z0-9]+)", ligne)
            if not match:
                raise ValueError(f"Ligne mal formatée : '{ligne}'")

            depart, symb, arrivee = match.group(1), match.group(2), match.group(3)
            initial = get_etat_id(depart)
            final = get_etat_id(arrivee)
            etats.update([initial, final])

            if initial not in transi:
                transi[initial] = {}
            if symb not in transi[initial]:
                transi[initial][symb] = []
            if final not in transi[initial][symb]:
                transi[initial][symb].append(final)

        for etat in etats:
            if etat not in transi:
                transi[etat] = {}

        self.alphabet = alphabet
        self.etats = etats
        self.entrees = entrees
        self.sorties = sorties
        self.transitions = transi

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
        transi.update({'P': {}})
        P = False
        for ligne in lignes[5:5 + nb_trans]:
            match = re.match(r"(\d+|P)([a-zA-Z]+)(\d+|P)", ligne)
            if match.group(1) == 'P':
                depart = match.group(1)
                P = True
            else:
                depart = int(match.group(1))
            if match.group(3) == 'P':
                arrivee = match.group(3)
                P = True
            else:
                arrivee = int(match.group(3))
            symbole = match.group(2)
            if symbole not in transi[depart]:
                transi[depart][symbole] = []
            transi[depart][symbole].append(arrivee)
        if P == True:
            P_int = len(etats)-1
            etats.remove(P_int)
            del transi[P_int]
            etats.append('P')
        else:
            del transi['P']
        self.alphabet = alphabet
        self.etats = etats
        self.entrees = entrees
        self.sorties = sorties
        self.transitions = transi

    def display(self):
        alphabet = sorted(self.alphabet)
        P = False
        if 'P' in self.etats:
            self.etats.remove('P')
            P = True
        etats = sorted(self.etats)
        if P == True:
            self.etats.append('P')
            etats.append('P')
        ent_etats = self.entrees
        sor_etats = self.sorties
        transitions = self.transitions

        # Définir la largeur de chaque colonne
        col_width = 6  # Ajustable selon la lisibilité souhaitée

        # En-tête avec l'alphabet
        header = " " * (col_width + 1) + "".join(sym.ljust(col_width) for sym in alphabet)
        print(header)
        print("=" * len(header))

        for etat in etats:
            # "E" pour initial, "S" pour terminal
            prefix = ""
            prefix += "E" if etat in ent_etats else " "
            prefix += "S" if etat in sor_etats else " "
            prefix += f"{etat}".ljust(col_width - 2)  # Aligne

            # Transitions pour chaque symbole de l'alphabet
            ligne = []
            for sym in alphabet:
                dests = transitions[etat].get(sym, [])
                cell = ",".join(map(str, sorted(dests))) if dests else "--"
                ligne.append(cell.ljust(col_width))

            print(prefix + " ".join(ligne))

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