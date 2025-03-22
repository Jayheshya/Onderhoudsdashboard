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

if eigenschappen_personeelslid["verlaagde_fysieke_belasting"] == None: # vult de maximum fysieke belasting in ALS deze ontbreekt       
    leeftijd = eigenschappen_personeelslid["leeftijd"]

    match leeftijd:
        case _ if leeftijd < 25:
            eigenschappen_personeelslid["verlaagde_fysieke_belasting"] = 25
        case _ if leeftijd > 50:
            eigenschappen_personeelslid["verlaagde_fysieke_belasting"] = 20
        case _:
            eigenschappen_personeelslid["verlaagde_fysieke_belasting"] = 40

# print(eigenschappen_personeelslid)
print("Naam werknemer:", eigenschappen_personeelslid["naam"])
print("Totale werktijd (in minuten):", eigenschappen_personeelslid["werktijd"])

# Vraag een overzicht van onderhoudstaken.
# Dit is een lijst met dicts. Dit is "dataset #2"

# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan en voeg queries toe om de juiste onderhoudstaken op te halen
select_query = 'SELECT * FROM attractiepark_onderhoud.Onderhoudstaak WHERE afgerond = 0 ORDER BY FIELD(bevoegdheid,"Senior","Medior","Junior","Stagiair") ASC, prioriteit ASC;'

onderhoudstaken = db.execute_query(select_query)

# altijd verbinding sluiten met de database als je klaar bent
db.close()

# bevoegdheden naar int
bevoegdheid = {
    "Stagiair": 1,
    "Junior": 2,
    "Medior": 3,
    "Senior": 4
}

dagtaken = []
restant_werktijd = eigenschappen_personeelslid["werktijd"]

# taken worden in vier aparte lijsten gezet zodat ze correct gesorteerd kunnen worden op basis van specialisatie en prioriteit
def filter_en_sorteren_taken(onderhoudstaken, medewerker):
    onderhoudstaken.sort(key=lambda t: (t["attractie"] != medewerker["specialist_in_attracties"], t["prioriteit"] != "hoog"))
    return onderhoudstaken

onderhoudstaken_gesorteerd = filter_en_sorteren_taken(onderhoudstaken, eigenschappen_personeelslid)

for onderhoudstaak in onderhoudstaken_gesorteerd:
    if onderhoudstaak["duur"] + 2 > restant_werktijd:
        continue
    if onderhoudstaak["beroepstype"] != eigenschappen_personeelslid["beroepstype"]:
        continue
    if bevoegdheid[eigenschappen_personeelslid["bevoegdheid"]] < bevoegdheid[onderhoudstaak["bevoegdheid"]]:
        continue

    onderhoudstaak["duur"] += 2
    dagtaken.append(onderhoudstaak)
    restant_werktijd -= onderhoudstaak["duur"]

# Voeg taken toe aan de dagtakenlijst en bereken de totale duur
totale_duur = 0
dagtakenlijst = []

for dagtaak in dagtaken:
    dagtakenlijst.append({
        "attractie": dagtaak["attractie"],
        "omschrijving": dagtaak["omschrijving"],
        "bevoegdheid": dagtaak["bevoegdheid"],
        "beroepstype": dagtaak["beroepstype"],
        "prioriteit": dagtaak["prioriteit"],
        "duur": dagtaak["duur"],
        "fysieke_belasting": dagtaak["fysieke_belasting"],
        "is_buitenwerk": dagtaak["is_buitenwerk"]
    })
    totale_duur += dagtaak["duur"]

persoonlijk_taken = {
     "personeelsgegevens": {
        "naam" : eigenschappen_personeelslid["naam"],
        "werktijd": eigenschappen_personeelslid["werktijd"],
        "beroepstype": eigenschappen_personeelslid["beroepstype"],
        "bevoegdheid": eigenschappen_personeelslid["bevoegdheid"],
        "Specialist in attracties": eigenschappen_personeelslid["specialist_in_attracties"],
        "Pauze opsplitsen": eigenschappen_personeelslid["pauze_opsplitsen"],
        "Maximale fysieke belasting (in kilo's)": eigenschappen_personeelslid["verlaagde_fysieke_belasting"]
     },
    "weergegevens" : {
        # vul aan met weergegevens
    }, 
    "dagtaken": dagtakenlijst # hier komt een lijst met alle dagtaken
    ,
    "totale_duur": totale_duur # aanpassen naar daadwerkelijke totale duur
}

# Schrijf het resultaat naar een JSON-bestand
output_bestand_pad = Path(__file__).parent / 'bbbb2.json'

with open(output_bestand_pad, 'w', encoding='utf-8') as json_bestand_uitvoer:
    json.dump(persoonlijk_taken, json_bestand_uitvoer, indent=4, ensure_ascii=False)

print(f"Dagtakenlijst opgeslagen in: {output_bestand_pad}")

