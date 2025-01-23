import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
def generate_barre_orizzontali(colors, labels, sizes):
    """
    Genera un grafico a barre orizzontali con colori personalizzati e restituisce l'immagine come array di byte.

    Args:
        colors (list): Lista di colori in formato "rgb(r, g, b)".
        labels (list): Etichette delle fette del grafico.
        sizes (list): Dimensioni delle fette del grafico.

    Returns:
        bytearray: L'immagine del grafico a barre in pila come array di byte.
    """

    # Crea il grafico a barre orizzontali
    fig, ax = plt.subplots()
    y_pos = np.arange(len(labels))
    ax.barh(y_pos, sizes, color=colors, edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)

    # Aggiungi le etichette ai bar
    for i, v in enumerate(sizes):
        ax.text(v + 0.1, i, str(v) + "%", color='black', va='center')


    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format='PNG')
    plt.close()

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()