import re
class AUTO():
    def __init__(self):
        self.alphabet = [] #liste qui contient les lettres de l'alphabet
        self.etats = [] #liste des états de l'automate
        self.entrees = [] #liste des états entrées
        self.sorties = [] #liste des états sorties
        self.transitions = {} #dico { états : { lettres : [états transitoires/arrivées] } }

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
        i = False
        if 'i' in self.etats:
            self.etats.remove('i')
            i = True
        etats = sorted(self.etats)
        if P == True:
            self.etats.append('P')
            etats.append('P')
        if i == True:
            self.etats.append('i')
            etats.append('i')
        ent_etats = self.entrees
        sor_etats = self.sorties
        transitions = self.transitions

        # Définir la largeur de chaque colonne
        col_width = 20  # Ajustable selon la lisibilité souhaitée

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

    def completion(self):
        if self.estComp() == True:
            return
        self.etats.append('P')
        self.transitions['P'] = {symbole: ['P'] for symbole in self.alphabet}
        for etat in self.etats:
            for symbole in self.alphabet:
                if symbole not in self.transitions.get(etat, {}):
                    self.transitions[etat][symbole] = ['P']

    def determinisation_completion(self):
        etats_a_ignorer = {'z'}

        # Convertir les états d'entrée en un tuple trié, en excluant les états à ignorer
        nouveaux_etats = [tuple(sorted(set(self.entrees) - etats_a_ignorer, key=lambda x: str(x)))]
        nouvelles_transitions = {}
        etats_a_traiter = [tuple(
            sorted(set(self.entrees) - etats_a_ignorer, key=lambda x: str(x)))]  # Initialiser avec les états d'entrée

        while etats_a_traiter:
            etat_courant = etats_a_traiter.pop()

            # Si l'état courant est vide, on l'ignore et on passe à l'itération suivante
            if not etat_courant:
                continue

            nouvelles_transitions[etat_courant] = {}

            for symbole in self.alphabet:
                # Collecter tous les états suivants pour chaque état courant et chaque symbole, en excluant les états à ignorer
                etats_suivants = set()
                for etat in etat_courant:
                    if etat not in etats_a_ignorer:  # Ignorer les états spéciaux
                        etats_suivants.update(self.transitions.get(etat, {}).get(symbole, set()))

                # Exclure les états à ignorer des états suivants
                etats_suivants -= etats_a_ignorer

                # Convertir l'ensemble en tuple trié avec une clé de tri personnalisée
                etats_suivants_tuple = tuple(sorted(etats_suivants, key=lambda x: str(x)))

                # Si l'état suivant est vide (i.e. un ensemble vide), on ne l'ajoute pas
                if etats_suivants_tuple:
                    nouvelles_transitions[etat_courant][symbole] = etats_suivants_tuple

                    if etats_suivants_tuple not in nouveaux_etats:
                        nouveaux_etats.append(etats_suivants_tuple)
                        etats_a_traiter.append(etats_suivants_tuple)

        # Filtrer les états vides
        nouveaux_etats = [etat for etat in nouveaux_etats if etat]  # Supprimer les états vides

        # Mettre à jour les propriétés de l'automate
        self.etats = nouveaux_etats
        self.transitions = nouvelles_transitions
        self.entrees = [tuple(sorted(set(self.entrees) - etats_a_ignorer, key=lambda x: str(x)))]
        self.sorties = [etat for etat in self.etats if any(s in etat for s in self.sorties)]

        # Complétion
        self.completion()
        print("L'automate a été déterminisé et complété.")

    def afficher_deterministe_complet(self):
        print(f"Alphabet : {self.alphabet}")

        print("\nÉtats de l automate et leur composition en états de l'automate d'origine :")
        for etat in self.etats:
            if isinstance(etat, tuple):
                composition = ".".join(str(e) for e in etat)  # Convertir en chaîne avec séparateur
            else:
                composition = str(etat)
            print(f"- {composition} : correspond à {etat}")

        print("\nÉtats initiaux :")
        for etat in self.entrees:
            if isinstance(etat, tuple):
                composition = ".".join(str(e) for e in etat)
            else:
                composition = str(etat)
            print(f"- {composition}")

        print("\nÉtats finaux :")
        for etat in self.sorties:
            if isinstance(etat, tuple):
                composition = ".".join(str(e) for e in etat)
            else:
                composition = str(etat)
            print(f"- {composition}")

        print("\nTransitions :")
        for etat, transitions in self.transitions.items():
            if isinstance(etat, tuple):
                etat_str = ".".join(str(e) for e in etat)
            else:
                etat_str = str(etat)
            for symbole, destination in transitions.items():
                if isinstance(destination, tuple):
                    destination_str = ".".join(str(e) for e in destination)
                else:
                    destination_str = str(destination)
                print(f"{etat_str} --{symbole}--> {destination_str}")
        self.display()

    def afficher_partitions(self, partition, step):
        print(f"\nÉtape {step} : Partition des états")
        for class_id, states in partition.items():
            print(f"  Groupe {class_id} : {sorted(states, key=lambda x: str(x))}")

    def minimisation(self):
        if self.estDeter() == False or self.estComp() == False:
            self.determinisation_completion()
        # Étape 1 : Initialisation des partitions (États finaux vs Non-finaux)
        partition = {}
        if self.sorties:
            partition[0] = set(self.sorties)
            partition[1] = set(self.etats) - partition[0]
        else:
            partition[0] = set(self.etats)  # Aucun état final

        self.afficher_partitions(partition, step=0)

        stable = False
        step = 1

        while not stable:
            stable = True
            new_partition = {}
            class_map = {}  # Dictionnaire pour suivre l'assignation des groupes
            class_counter = 0

            for state in self.etats:
                # Clé = (groupe d'appartenance, transitions vers groupes pour chaque symbole)
                groupe_actuel = next((g for g, contenu in partition.items() if state in contenu), -1)
                transitions_classes = tuple(
                    next(
                        (g for g, contenu in partition.items() if
                         next(iter(self.transitions[state].get(sym, [-1])), -1) in contenu),
                        -1
                    ) for sym in sorted(self.alphabet)
                )
                key = (groupe_actuel, transitions_classes)

                # Création du groupe si la clé est nouvelle
                if key not in class_map:
                    class_map[key] = class_counter
                    class_counter += 1

                new_groupe = class_map[key]
                new_partition.setdefault(new_groupe, set()).add(state)

            if len(new_partition) != len(partition) or any(
                    new_partition[k] != partition.get(k, set()) for k in new_partition):
                stable = False
                self.afficher_partitions(new_partition, step)
                step += 1
            else:
                print("\nL’automate est minimal.")

            partition = {k: v.copy() for k, v in new_partition.items()}

        # Étape 2 : Construction de l'automate minimal
        state_map = {state: class_id for class_id, states in partition.items() for state in states}
        min_transitions = {}

        for class_id, states_in_group in partition.items():
            rep = next(iter(states_in_group))
            min_transitions[class_id] = {}
            for sym in sorted(self.alphabet):
                dests = self.transitions[rep].get(sym, [])
                if dests:
                    target = next(iter(dests))

                    if target not in state_map:
                        state_map[target] = target

                    min_transitions[class_id][sym] = state_map[target]

        # Mise à jour de l'automate
        self.etats = set(partition.keys())
        self.transitions = min_transitions
        self.entrees = [state_map[next(iter(self.entrees))]]
        self.sorties = [cid for cid, states in partition.items() if states & set(self.sorties)]

        print("\nAutomate minimal obtenu :")
        self.afficher_automate_minimal()

    def afficher_automate_minimal(self):
        # Affiche l'automate minimisé sous un format lisible

        alphabet = sorted(self.alphabet)
        states = sorted(self.etats)
        init_states = self.entrees
        final_states = self.sorties
        transitions = self.transitions

        col_width = 6  # Largeur uniforme pour un bon alignement
        header = " " * (col_width + 1) + "".join(sym.ljust(col_width) for sym in alphabet)
        print(header)
        print("=" * len(header))  # séparation

        for state in states:
            prefix = ""
            prefix += "E" if state in init_states else " "
            prefix += "S" if state in final_states else " "
            prefix += f"{state}".ljust(col_width - 2)  # Alignement

            ligne = []
            for sym in alphabet:
                dest = transitions[state].get(sym, "--")
                ligne.append(f"{str(dest).ljust(col_width)}")

            print(prefix + " ".join(ligne))

    def reconnaitre_mot(self, mot):
        current_state = next(iter(self.entrees))  # On part du seul état initial

        for char in mot:
            if char not in self.alphabet:
                print(f"Symbole '{char}' absent de l'alphabet")
                return False
            dests = self.transitions.get(current_state, {}).get(char, None)
            if dests is None:
                return False
            # Si c'est une liste, on prend le 1er élément, sinon on suppose que c'est un int
            current_state = dests[0] if isinstance(dests, list) else dests
        # Automate déterministe → un seul état d'arrivée

        return current_state in self.sorties

    def lire_mot(self):
        print("\nEntrer des mots à tester, taper 'fin' pour quitter :")
        while True:
            mot = input("→ Mot : ").strip()
            if mot.lower() == "fin":
                print("Fin de la lecture des mots.")
                break
            if self.reconnaitre_mot(mot):
                print("Mot recconnu")
            else:
                print("inconnu au bataillon! Je rigole. Mot Non-recconnu")

    def complementaire(self):
        new_sorties = [etat for etat in self.etats if etat not in self.sorties]
        self.sorties = new_sorties
        print("Voici l'automate complémentaire")
        self.display()

    def auto_copy(self):
        copy_auto = AUTO()
        copy_auto.alphabet = self.alphabet
        copy_auto.etats = self.etats
        copy_auto.entrees = self.entrees
        copy_auto.sorties = self.sorties
        copy_auto.transitions = self.transitions
        return copy_auto
