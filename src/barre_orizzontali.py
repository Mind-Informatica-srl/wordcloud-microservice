import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from constants import EMU

# Importa il font manager di Matplotlib
from matplotlib import font_manager as fm
def generate_barre_orizzontali(colors, labels, sizes, format, width, height):
    """
    Genera un grafico a barre orizzontali con colori personalizzati e restituisce l'immagine come array di byte.

    Args:
        colors (list): Lista di colori in formato "rgb(r, g, b)".
        labels (list): Etichette delle fette del grafico.
        sizes (list): Dimensioni delle fette del grafico.

    Returns:
        bytearray: L'immagine del grafico a barre in pila come array di byte.
    """

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 14
        height = 6
    else:
        width = width / EMU
        height = height / EMU

    if not sizes or not colors or not labels or sizes.count(0) == len(sizes) or sizes is None or colors is None or labels is None:
        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(800, 600))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            byte_io.write(dwg.tostring().encode('utf-8'))
            byte_io.seek(0)
            return byte_io.read()
        else:
            img = Image.new('RGB', (800, 600), color='white')
            font_path = "fonts/Figtree-VariableFont_wght.ttf"
            try:
                font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
            except IOError:
                font = ImageFont.load_default()  # Usa font di default se non trovato

            draw = ImageDraw.Draw(img)
            draw.text((400, 300), "Nessun dato disponibile", fill="black", font=font, anchor='mm')
            byte_io = io.BytesIO()
            img.save(byte_io, format=format)
            byte_io.seek(0)
            return byte_io.read()

    # Crea il grafico a barre orizzontali
    fig, ax = plt.subplots(figsize=(width, height))
    y_pos = np.arange(len(labels))
    bar_height = 0.4  # Altezza delle barre
    ax.barh(y_pos, sizes, color=colors, edgecolor=None, height=bar_height)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10, fontweight='bold', fontproperties=avenir_font_path)

    # Imposta il limite massimo dell'asse delle ascisse a 100
    ax.set_xlim(0, 100)

    # Aggiungi il simbolo delle percentuali all'asse delle ascisse
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))

    # Aggiungi le etichette ai bar
    for i, v in enumerate(sizes):
        v = round(v)
        ax.text(v + 0.1, i, f"{v}%", color='black', va='center', fontsize=10, fontweight='bold', fontproperties=avenir_font_path)

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
    plt.savefig(byte_io, format=format)
    plt.close()

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()