def calculateenergy(gesamt_energie_kcal):
    """
    Funktion rechnet den metabolischen Energieverbrauch aus Lab2functions.py um in alternative Einheiten
    - Joule 
    - Kilokalorien (kcal)
    - Rittersporttafeln (100g Tafel = 541 kcal)
    - Bier (0.5l Glas = 210 kcal)
    - Anteil am Tagesbedarf von Lasse
    """
    gewicht_lasse = 59  # kg
    groesse_lasse = 178  # cm
    alter_lasse = 19  # Jahre
    tagesbedarf_lasse_kcal = (66.47+(13.75*gewicht_lasse)+(5*groesse_lasse)-(6.755*alter_lasse))*1.375 

    # Umrechnung in Joule
    energie_joule = gesamt_energie_kcal * 4184  # 1 kcal = 4184 Joule

    # Umrechnung in Kilokalorien (kcal)
    energie_kcal = gesamt_energie_kcal  # bereits in kcal

    # Umrechnung in Rittersporttafeln (100g Tafel = 541 kcal)
    energie_rittersport = energie_kcal / 541

    # Umrechnung in Bier (0.5l Glas = 210 kcal)
    energie_bier = energie_kcal / 210

    # Anteil am Tagesbedarf von Lasse (ca. 2500 kcal pro Tag)
    anteil_tagesbedarf = (energie_kcal / tagesbedarf_lasse_kcal) * 100  # in Prozent

    print("Joule:", energie_joule,
        "Kilokalorien:", energie_kcal,
        "Rittersporttafeln:", energie_rittersport,
        "Bier (0.5l Gläser):", energie_bier,
        "Anteil am Tagesbedarf (%):", anteil_tagesbedarf
    )