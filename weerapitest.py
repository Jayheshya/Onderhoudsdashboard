import requests
import json

def haal_weergegevens_op(station="260"):
    # """
    # Haalt actuele weersgegevens op van KNMI voor een bepaald weerstation.
    # Standaard station 260 (De Bilt).
    # """
    url = f"https://weerlive.nl/api/json-data-10min.php?key=eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjU4NzE3YzkzOWMwYzQwMTdiN2JmNDgwMjEyNzM3NDY5IiwiaCI6Im11cm11cjEyOCJ9&locatie={station}"
    

    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weer_info = data["liveweer"][0]
            return {
                "temperatuur": weer_info["temp"],
                "neerslag": weer_info["d0neerslag"],
                "windkracht": weer_info["d0windk"],
                "omschrijving": weer_info["samenv"]
            }
        else:
            print("Fout bij ophalen van weergegevens:", response.status_code)
            return None

    except Exception as e:
        print("Er ging iets mis:", e)
        return None
