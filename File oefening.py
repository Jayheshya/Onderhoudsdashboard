
bestandnaam = input("bestandnaam:\n")
getal = input("Voer een getal in:\n")
with open(bestandnaam, "+a") as bestand:
    n = bestand.write(f"{getal}\n")


    