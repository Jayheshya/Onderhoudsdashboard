# import modulen
from pathlib import Path
import json
import pprint
from database_wrapper import Database

# Definitie functies

# initialisatie

# parameters voor connectie met de database
db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_onderhoud")

# main

# Haal de eigenschappen op van een personeelslid .
# navigeer naar het JSON-bestand, let op: er zijn ook andere personeelsleden om te testen!
# en maak vooral ook je eigen persoonlijke voorkeuren :-)
bestand_pad = Path(__file__).parent / 'personeelsgegevens_personeelslid_1.json' #'personeelsgegevens_personeelslid_1.json'

# open het JSON-bestand 
json_bestand = open(bestand_pad)

# zet het om naar een Python-dictionary
eigenschappen_personeelslid = json.load(json_bestand)

json_bestand.close() # sluit het bestand

print(eigenschappen_personeelslid)
print(eigenschappen_personeelslid["naam"])

# Vraag een overzicht van onderhoudstaken.
# Dit is een lijst met dicts. Dit is "dataset #2"

# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan en voeg queries toe om de juiste onderhoudstaken op te halen
select_query = "SELECT * FROM attractiepark_onderhoud.onderhoudstaak WHERE afgerond = 0 ORDER BY prioriteit;"
onderhoudstaken = db.execute_query(select_query)

# altijd verbinding sluiten met de database als je klaar bent
db.close()

pprint.pp(onderhoudstaken)

# DE OPDRACHT
# Met die 2 datasets moet je tot een dagtakenlijst komen voor het personeelslid
# Zorg dat je een algoritme ontwikkelt, conform eisen in het ontwerpdocument
# Zorg dat het een dagtakenlijst genereert/output naar een .json bestand,
# dat weer ingelezen kan worden in een webomgeving (zie acceptatieomgeving website folder)
# Hieronder een begin...

persoonlijk = {
    "personeelsgegevens" : {
        "naam": eigenschappen_personeelslid["naam"]
        # vul aan met andere benodigde eigenschappen
    },
    "weergegevens" : {
        # vul aan met weergegevens
    }, 
    "dagtaken": [] # hier komt een lijst met alle dagtaken
    ,
    "totale_duur": 0 # aanpassen naar daadwerkelijke totale duur0
}

# uiteindelijk schrijven we de dictionary weg naar een JSON-bestand
with open('dagtakenlijst_personeelslid_x.json', 'w') as json_bestand_uitvoer:
    json.dump(dagtakenlijst, json_bestand_uitvoer, indent=4)
