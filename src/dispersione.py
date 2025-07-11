import matplotlib

from funzioni_shared import calcola_font_size
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text
import io
import textwrap
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from constants import EMU
import numpy as np

# Importa il font manager di Matplotlib
from matplotlib import font_manager as fm

# Dati
x = [1, 2, 1.5, 3, 2.5, 4, 4.5, 5, 2, 1, 1.2, 3.8, 4.2, 1.3, 0.8]  # Importanza
y = [0.5, 1, 1.5, 1.8, 2.5, 2.8, 3.5, 4, 1.2, 1.8, 0.7, 3.2, 3.8, 0.9, 0.4]  # Frequenza di scelta
labels = [
    "Utilità del lavoro", "Senso di appartenenza", "Rapporto con l'Azienda", 
    "Ambiente di lavoro", "Orario di lavoro", "Quantità di lavoro",
    "Pianificazione del lavoro", "Prospettive di carriera", "Relazioni colleghi",
    "Autonomia e responsabilità inadeguate", "Identificazione Luxury", 
    "Cultura organizzativa", "Equilibrio tra lavoro e vita privata", 
    "Scarsa chiarezza dei ruoli", "Valutazione"
]
def generate_dispersione(x, y, labels, format, width, height):

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 14
        height = 7
    else:
        width = width / EMU
        height = height / EMU

    font_size = calcola_font_size(width, height)
    
    if not x or not y or not labels or len(x) != len(y) or len(x) != len(labels) or len(y) != len(labels) or all(value == 0 for value in x) or all(value == 0 for value in y) or x is None or y is None or labels is None: 
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
    
    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(width, height))  # Imposta la dimensione della figura per renderla più stretta in altezza

    np.random.seed(42)
    jitter_strength = 1.5
    x_jittered = [xi + np.random.uniform(-jitter_strength, jitter_strength) for xi in x]
    y_jittered = [yi + np.random.uniform(-jitter_strength, jitter_strength) for yi in y]

    # Aggiunta dei punti
    ax.scatter(x, y, color='red')
    # Aggiunta delle etichette ai punti
    metaX = 50
    metaY = 50
    for i, label in enumerate(labels):
        radius = 4
        vicini_sopra = [j for j in range(len(x)) if j != i and abs(x[i] - x[j]) < radius and y[j] > y[i] and abs(y[i] - y[j]) < radius]
        vicini_sotto = [j for j in range(len(x)) if j != i and abs(x[i] - x[j]) < radius and y[j] < y[i] and abs(y[i] - y[j]) < radius]
        vicini_dx = [j for j in range(len(x)) if j != i and x[j] > x[i] and abs(x[i] - x[j]) < radius and abs(y[i] - y[j]) < radius]
        vicini_sx = [j for j in range(len(x)) if j != i and x[j] < x[i] and abs(x[i] - x[j]) < radius and abs(y[i] - y[j]) < radius]

        base_offset = 2
        offset_x = 1.5
        # Default
        ha = 'left'
        va = 'center'
        offset_y = 0

        if not vicini_sopra and not vicini_sotto and not vicini_dx and not vicini_sx:
            offset_x = 2
            offset_y = 0
            ha = 'left'
            va = 'center'
        else:
            # Verticale
            if len(vicini_sopra) > len(vicini_sotto):
                offset_y = -base_offset * (1 + len(vicini_sopra))
                va = 'top'
            else:
                offset_y = base_offset * (1 + len(vicini_sotto))
                va = 'bottom'
            # Orizzontale
            if len(vicini_dx) > len(vicini_sx):
                offset_x = -base_offset * (1 + len(vicini_dx))
                ha = 'right'
            else:
                offset_x = base_offset * (1 + len(vicini_sx))
                ha = 'left'

        wrapped_label = "\n".join(textwrap.wrap(label, width=30))
        ax.annotate(
            wrapped_label,
            (x[i], y[i]),
            xytext=(x[i]+offset_x, y[i]+offset_y),
            textcoords='data',
            fontsize=12,
            fontweight='bold',
            fontproperties=avenir_font_path,
            arrowprops=dict(arrowstyle="->", color='gray', lw=0.5),
            zorder=10,
            verticalalignment=va,
            horizontalalignment=ha
        )

    # Sposta le etichette solo se necessario e mostra la freccia solo se serve
    # Chiama adjust_text per spostare le etichette evitando sovrapposizioni
    # adjust_text(texts, x=x, y=y, autoalign='y',force_text=0.5,
    #     force_points=0.5, only_move={'points':'xy', 'texts':'xy'}, 
    #     expand_points=(1.5, 1.5), expand_text=(2, 2))

    # Aggiunta delle linee per dividere il grafico in 4 parti uguali
    ax.axhline(y= metaY, color='lightgrey', linestyle='-', zorder=0)
    ax.axvline(x= metaX, color='lightgrey', linestyle='-', zorder=0)

    # Aggiungere su ogni riquadro creato un'etichetta, se il riquadro è in basso si mette sulla base
    # se è in alto si mette sopra
    # Etichette per i quadranti
    quartoquadrante = 12.5
    primoquarto = quartoquadrante
    terzoquarto = 65
    ax.text(primoquarto, 102, "A. NON IMPORTANTI E SCELTE DA MOLTI", fontsize=font_size, fontweight='bold', backgroundcolor='darkgreen', color='white', fontproperties=avenir_font_path)
    ax.text(terzoquarto, 102, "B. IMPORTANTI E SCELTE DA MOLTI", fontsize=font_size, fontweight='bold', backgroundcolor='darkgreen', color='white', fontproperties=avenir_font_path)
    # Aggiungi un cerchio rosso sopra l'etichetta
    circle = patches.Ellipse((75.8, 102.6), width=30,height=8, edgecolor='red', facecolor='none', linewidth=2, zorder=10, clip_on=False)
    ax.add_patch(circle)
    ax.text(primoquarto, -10, "C. NON IMPORTANTI E SCELTE DA POCHI", fontsize=font_size, fontweight='bold', backgroundcolor='darkgreen', color='white', fontproperties=avenir_font_path)
    ax.text(terzoquarto, -10, "D. IMPORTANTI E SCELTE DA POCHI", fontsize=font_size, fontweight='bold', backgroundcolor='darkgreen', color='white', fontproperties=avenir_font_path)



    # Personalizzazioni
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 102)
    ax.set_xlabel("IMPORTANZA", fontsize=font_size, labelpad=10, fontweight='bold', fontproperties=avenir_font_path)
    ax.set_ylabel("FREQUENZA DI SCELTA", fontsize=font_size, labelpad=10, fontweight='bold', fontproperties=avenir_font_path)
    ax.spines['top'].set_color('green')
    ax.spines['right'].set_color('green')
    ax.spines['left'].set_color('green')
    ax.spines['bottom'].set_color('green')
    ax.tick_params(axis='both', which='both', color='green')
    ax.tick_params(axis='x', pad=12)

    # Imposta il colore del contorno a verde
    for spine in fig.gca().spines.values():
        spine.set_edgecolor('green')

    # Rimuovi le etichette degli assi
    # fig.gca().set_xticklabels([])
    # fig.gca().set_yticklabels([])

    # Titolo
    # plt.title("Distribuzione Importanza-Frequenza", fontsize=14, pad=15)

    # Salvataggio e visualizzazione
    fig.tight_layout()

    byte_io = io.BytesIO()
    fig.savefig(byte_io, format=format, bbox_inches="tight")
    plt.close(fig)

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()
