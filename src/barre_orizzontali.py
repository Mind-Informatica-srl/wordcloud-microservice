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
    fig, ax = plt.subplots(figsize=(14,6))
    y_pos = np.arange(len(labels))
    bar_height = 0.2  # Altezza delle barre
    ax.barh(y_pos, sizes, color=colors, edgecolor=None, height=bar_height)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)

    # Imposta il limite massimo dell'asse delle ascisse a 100
    ax.set_xlim(0, 100)

    # Aggiungi il simbolo delle percentuali all'asse delle ascisse
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))

    # Aggiungi le etichette ai bar
    for i, v in enumerate(sizes):
        ax.text(v + 0.1, i, f"{v:.2f}%", color='black', va='center', fontsize=10)

    # Riduci lo spazio tra le barre
    ax.set_ylim(-0.5, len(labels) - 0.5)

    # Rimuovi il bordo esterno del grafico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Aggiungi linee grigie chiare per ogni etichetta dell'asse delle ascisse
    ax.grid(axis='x', color='lightgrey', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # Posiziona le linee della griglia dietro le barre

    # Adatta il layout del grafico
    plt.tight_layout()

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format='PNG')
    plt.close()

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()