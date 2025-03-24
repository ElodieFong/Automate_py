from automate import AUTO

auto = AUTO()
print("Numéro de l'automate: ")
num = input()
auto.insert("num_automate/" + str(num) + ".txt")

print()
print("===================================================")
print("===================================================")
print("===================================================")
auto.display()
print("===================================================")
print("===================================================")
print("===================================================")

run = True
while run:

    matrice = []
    Deter = 0
    Comp = 0
    Stand = 0
    for loop in range(10):
        print()
    # Vérification de l'état de l'automate
    if auto.estDeter():
        print("L'automate est déterminisé")
        Deter = 0
    else:
        print("L'automate n'est pas déterminisé")
        Deter = 1

    if auto.estStand():
        print("L'automate est standardisé")
        matrice.append("Afficher l'automate standardisé")
        Stand = 0
    else:
        print("L'automate n'est pas standardisé")
        matrice.append("Standardiser l'automate")

    if auto.estComp():
        print("L'automate est complété")
        Comp = 0
    else:
        print("L'automate n'est pas complété")
        Comp = 1

    # Ajout des options en fonction de l'état de l'automate
    if Deter == 1 and Comp == 1:
        matrice.append("Déterminiser et Compléter l'automate")
    else:
        matrice.append("Afficher l'automate déterminisé et complété")

    matrice.append("Minimiser l'automate")
    matrice.append("Afficher Automate Complementaire")
    matrice.append("Lire Mot")
    matrice.append("Reconnatire Mot")
    matrice.append("Quitter")


    # Boucle du menu
    print("\n===================================================")
    print("Menu :\n")
    for i, item in enumerate(matrice, start=1):
        print(f"{i}. {item}")
    print()

    try:
        choix = int(input("Que voulez-vous faire ? ").strip())
        print("\n===================================================")

    except ValueError:
        print("Veuillez entrer un nombre valide.")
        continue

    if choix == 1:
        if "Standardiser" in matrice[0]:  # Vérifier la présence de l'option
            auto.standardisation()
        else:
            auto.display()

    elif choix == 2:
        if "Déterminiser et Compléter" in matrice[1]:
            print("\n== Déterminisation et complétion ==")
            auto.determinisation_completion()
        else:
            print("\n== Affichage de l'automate déterminisé et complété ==")
            auto.afficher_deterministe_complet()

    elif choix == 3:
        auto.minimisation()

    elif choix == 4:
        auto.complementaire()

    elif choix == 5:
        auto.lire_mot()

    elif choix == 6:
        auto.reconnaitre_mot()

    elif choix == 7:
        run = False
        print("Fermeture du programme...")

    else:
        print("Choix invalide, veuillez entrer un nombre valide.")