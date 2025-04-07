import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image, ImageDraw, ImageFont
import svgwrite
# Importa il font manager di Matplotlib
from matplotlib import font_manager as fm
from constants import EMU

def generate_pie3d(colors, labels, sizes, explode, title, format, width, height):
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

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 14
        height = 6
    else:
        width = width / EMU
        height = height / EMU

    if not colors or not sizes or not labels or sizes.count(0) == len(sizes): 
        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(400, 300))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            dwg.write(byte_io, pretty=True)
            byte_io.seek(0)
            return byte_io.read()
        else:
            img = Image.new('RGB', (400, 300), color='white')
            font_path = "fonts/Figtree-VariableFont_wght.ttf"
            try:
                font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
            except IOError:
                font = ImageFont.load_default()  # Usa font di default se non trovato

            draw = ImageDraw.Draw(img)
            draw.text((200, 150), "Nessun dato disponibile", fill="black", font=font, anchor='mm')
            byte_io = io.BytesIO()
            img.save(byte_io, format=format)
            byte_io.seek(0)
            return byte_io.read()

    # Crea il grafico a torta tridimensionale
    plt.figure(figsize=(width, height))
    wedges, texts = plt.pie(
    sizes, labels=labels, explode=explode, shadow=False, colors=colors, startangle=0,
    labeldistance=1.1)

    # Calcola le percentuali
    total = sum(sizes)
    percentages = ['{:.2f}%'.format(100 * size / total) for size in sizes]


    # Aggiungi il titolo al grafico
    plt.title(title, fontproperties=avenir_font_path, fontsize=16, fontweight='bold')

    # Imposta il colore delle etichette e aggiungi le percentuali sotto le etichette
    for text, percentage, color in zip(texts, percentages, colors):
        text.set_fontweight('bold')
        text.set_fontproperties(avenir_font_path)
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

    