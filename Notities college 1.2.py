temp = 0
dag = int(input("Welke dag van de week is het? "))
uur = int(input("Hoe laat is het? "))

# weekdag opties
if dag >= 1 and dag <= 5:
    if uur >= 0 and uur <= 18:
        temp = 16
    elif uur > 18 and uur <= 23:
        temp = 19

# weekend opties
elif dag == 6 or dag == 7:
    if uur >= 0 and uur <= 12:
        temp = 16
    elif uur >= 13 and uur <= 23:
        temp = 19

print(f"De temperatuur is {temp} graden celcius")