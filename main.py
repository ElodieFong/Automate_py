from automate import AUTO
#problème: 41(la poubelle)
#auto non standard: 05, 06, 11, 12, 15, 39, 42...
auto = AUTO()
print("Numéro de l'automate: ")
num = input()
auto.insert("num_automate/" + str(num) + ".txt")
auto.display()
'''
if auto.estStand() == True:
    print("L'automate est standard")
else:
    print("L'automate n'est pas standard")
    auto.standardisation()
'''
if not auto.estDeter():
    print("\n== Déterminisation et complétion ==")
    auto.determinisation_completion()
    auto.afficher_deterministe_complet()
else:
    if not auto.estComp():
        print("\n== Complétion ==")
        auto.completion()
        auto.display()
    else:
        print("\nL'automate est déjà déterministe et complet.")
'''
auto.minimisation()
auto.afficher_automate_minimal()
'''