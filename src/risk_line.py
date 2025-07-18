import matplotlib

from funzioni_shared import calcola_font_size
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from constants import EMU

# Importa il font manager di Matplotlib
from matplotlib import font_manager as fm

def create_risk_line_chart(categories, values, risk_zones, risk_colors, legend_labels, color_categories, format, is_white, width, height):
    """
    Crea un grafico a linea con fasce di rischio sullo sfondo.

    :param categories: Lista di stringhe, nomi delle categorie (asse X).
    :param values: Lista di valori corrispondenti a ogni categoria.
    :param risk_zones: Lista di tuple, ogni tuple rappresenta (inizio, fine) per una fascia di rischio.
    :param risk_colors: Lista di stringhe, colori delle fasce di rischio.
    :param legend_labels: Lista di stringhe, etichette della leggenda delle fasce di rischio.
    """

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 14
        height = 7
    else:
        width = width / EMU
        height = height / EMU

    font_size = calcola_font_size(width, height)
    
    if not categories or not values or not risk_zones or not risk_colors or not legend_labels or len(values) == 0 or all(value == 0 for value in values) or is_white:
        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(400, 300))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            byte_io.write(dwg.tostring().encode('utf-8'))
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
    
    x_positions = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(width, height))

    # Aggiungi le fasce di rischio come sfondo
    risk_patches = []
    for i, (start, end) in enumerate(risk_zones):
        patch = ax.axhspan(start, end, color=risk_colors[i], alpha=1, label=f"{legend_labels[i]}")
        risk_patches.append(patch)

    # Disegna la linea
    ax.plot(x_positions, values, color="black", linewidth=2)

    # Aggiungi i valori sopra i punti
    for x, y in zip(x_positions, values):
        ax.text(x, y + 3, f"{y:.2f}", ha="center", fontsize=font_size, color="black", fontweight="bold", fontproperties=avenir_font_path)

    # Configura assi e legenda
    ax.set_xticks(x_positions)
    ax.set_xticklabels([label.replace("'\n'", "\n") for label in categories], rotation=45, ha="right", fontsize=font_size, fontweight="bold", fontproperties=avenir_font_path)
    for tick_label, color in zip(ax.get_xticklabels(), color_categories):
        tick_label.set_color(color)
        
    ax.set_ylim(0, max(risk_zones[-1]) + 10)
    # Aggiungi la legenda per le fasce di rischio lateralmente al grafico
    ax.legend(handles=risk_patches[::-1], loc="center left", bbox_to_anchor=(1, 0.5), title="Fasce di Rischio", title_fontsize="medium", frameon=False, prop=avenir_font_path)

    # Rimuovi il bordo nero intorno all'area del grafico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Mostra il grafico
    fig.tight_layout()

    byte_io = io.BytesIO()
    fig.savefig(byte_io, format=format)
    plt.close(fig)

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()


# # Esempio di utilizzo
# categories = [
#     "Identificazione Luxury", "Eventi e Peak Season", "Carico di Lavoro", "Orario di Lavoro", 
#     "Autonomia", "Ruolo", "Ambiente", "Pianificazione del Lavoro", 
#     "Relazioni", "Cultura Organizzativa", "Equilibrio Casa-Lavoro", "Sviluppo Professionale"
# ]
# values = [99.47, 103.19, 100.57, 106.14, 97.75, 102.25, 98.22, 103.91, 97.84, 101.14, 103.44, 99.11]
# risk_zones = [(0, 80), (80, 95), (95, 105), (105, 120), (120, 160)]
# risk_colors = ["#4CAF50", "#8BC34A", "#FFEB3B", "#FFC107", "#F44336"]
# legend_labels = ["Basso <80", "Medio-basso 80-95", "Medio 95-105", "Medio-alto 105-120", "Alto >120"]

# create_risk_line_chart(categories, values, risk_zones, risk_colors, legend_labels)