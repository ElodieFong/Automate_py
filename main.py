from automate import AUTO
#problème: 41(la poubelle)
auto = AUTO()
print("Numéro de l'automate: ")
num = input()
auto.insert("num_automate/" + str(num) + ".txt")
auto.display()
auto.estComp()
auto.estDeter()
if auto.estStand() == True:
    print("L'automate est standard")
else:
    print("L'automate n'est pas standard")