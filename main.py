from automate import AUTO
#problème: 41(la poubelle)
#auto non standard: 05, 06, 11, 12, 15, 39, 42...
auto = AUTO()
print("Numéro de l'automate: ")
num = input()
auto.insert("num_automate/" + str(num) + ".txt")
auto.display()
print("deter? ", auto.estDeter())
'''
if auto.estStand() == True:
    print("L'automate est standard")
else:
    print("L'automate n'est pas standard")
    auto.standardisation()
auto.complementaire()
'''
if not auto.estDeter():
    print("\n== Déterminisation et complétion ==")
    auto.determinisation_et_completion_automate()
else:
    if not auto.estComp():
        print("\n== Complétion ==")
        auto.completion()
    else:
        print("\nL'automate est déjà déterministe et complet.")
print("\n== Automate déterminisé et complet ==")
auto.afficher_automate_deterministe_complet()
auto.minimisation()
auto.afficher_automate_minimal()