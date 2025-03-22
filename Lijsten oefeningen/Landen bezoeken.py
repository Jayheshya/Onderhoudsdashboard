aantal_landen = int(input("Hoeveel landen heb je bezocht? "))
bezochte_landen = ["NL"]

for i in range (aantal_landen):
    land = input("Noem één land dat je hebt bezocht: ")   
    bezochte_landen.append(land)

print(bezochte_landen)