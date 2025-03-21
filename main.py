from automate import AUTO

auto = AUTO()
print("Numéro de l'automate: ")
num = int(input())
auto.insert("num_automate/" + str(num) + ".txt")
auto.display()