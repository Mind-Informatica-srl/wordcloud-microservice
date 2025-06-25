def calcola_font_size(larghezza, altezza):
    max_font_size = 14  # Dimensione massima del font
    if larghezza is None or altezza is None or larghezza <= 10 or altezza <= 5:
        return 12
    # Usa il valore minore tra larghezza e altezza per la proporzione
    base = min(larghezza, altezza)
    font_size = base // 2   # Imposta 10 come dimensione minima
    font_size = min(max_font_size, font_size)  # Assicura che non superi la dimensione massima
    return font_size