import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io


def generate_pie3d(colors, labels, sizes, explode, title, format):
    """
    Genera un grafico a torta tridimensionale con colori personalizzati e restituisce l'immagine come array di byte.

    Args:
        colors (list): Lista di colori in formato "rgb(r, g, b)".
        labels (list): Etichette delle fette del grafico.
        sizes (list): Dimensioni delle fette del grafico.
        explode (list): Esplosione delle fette del grafico.
        title (str): Titolo del grafico.

    Returns:
        bytearray: L'immagine del grafico a torta tridimensionale come array di byte.
    """

    if not colors or not sizes or not labels: 
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_axis_off()
        ax.text(0.5, 0.5, 'Dati Mancanti', horizontalalignment='center', verticalalignment='center', fontsize=20, color='red', transform=ax.transAxes)
        plt.tight_layout()
        byte_io = io.BytesIO()
        plt.savefig(byte_io, format=format)
        plt.close()
        byte_io.seek(0)
        return byte_io.read()

    # Crea il grafico a torta tridimensionale
    plt.figure(figsize=(14, 6))
    wedges, texts = plt.pie(
    sizes, labels=labels, explode=explode, shadow=False, colors=colors, startangle=0,
    labeldistance=1.1)

    # Calcola le percentuali
    total = sum(sizes)
    percentages = ['{:.2f}%'.format(100 * size / total) for size in sizes]


    # Aggiungi il titolo al grafico
    plt.title(title)

    # Imposta il colore delle etichette e aggiungi le percentuali sotto le etichette
    for text, percentage, color in zip(texts, percentages, colors):
        if percentage != '0.00%':
            text.set_color(color)
            text.set_fontsize(10)
            text.set_text(f'{text.get_text()}\n{percentage}')
        else:
            text.set_text('')

    # Adatta il layout del grafico
    plt.tight_layout()




    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format=format)
    plt.close()

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()

    