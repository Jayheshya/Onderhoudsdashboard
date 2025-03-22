import json
from urllib import request


url = "https://www.daggegevens.knmi.nl/klimatologie/uurgegevens"


with request.urlopen(url) as url_data:
    json_string = url_data.read().decode()
    gegevens = json.loads(json_string)


    print(gegevens)