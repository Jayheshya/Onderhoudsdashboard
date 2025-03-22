# tel getallen bij elkaar op, start bij startgetal t/m eindgetal

def tel_op(startgetal: int, eindgetal: int) -> int:
    totaal = 0
    for index in range(startgetal, eindgetal + 1):
        totaal = totaal + index

    return totaal

# Hyposcheiße
start = 2
eind = 6
verwachte_waarde = 20

print(tel_op(2,6))