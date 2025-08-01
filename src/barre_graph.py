import matplotlib

from funzioni_shared import calcola_font_size
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from matplotlib import font_manager as fm
from constants import EMU

def generate_barre_in_pila(cod_domanda, colors, labels, sizes, format, width, height, fasce_basse, fasce_alte):
    """
    Genera un grafico a barre in pila con colori personalizzati e restituisce l'immagine come array di byte.

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
        width = 10
        height = 3
    else:
        width = width / EMU
        height = height / EMU
    
    font_size = calcola_font_size(width, height)
    if not colors or not sizes or not labels or sizes.count(0) == len(sizes): 
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
        
    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(width, height))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    # for i in range(len(normalized_sizes)):
    #     ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None, height=0.6)
    #     if normalized_sizes[i] != 0:
    #         ax.text(left + normalized_sizes[i] / 2, 0.4, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=12, fontweight='bold')
    #     left += normalized_sizes[i]
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None)
        if normalized_sizes[i] != 0:
            ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=font_size, fontweight='bold', fontproperties=avenir_font_path)
        left += normalized_sizes[i]

    # Personalizzazioni
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xticklabels([f"{i}%" for i in range(0, 101, 20)], fontproperties=avenir_font_path)
    ax.set_yticks([]) 

    # Aggiungi margine inferiore
    ax.margins(y=0.2)

    # Aggiungi la legenda sotto l'asse delle x
    ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(labels), frameon=False, prop=avenir_font_path)


    # Rimuovi i bordi del grafico
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    # Rendi l'asse delle ascisse più chiara
    ax.spines['bottom'].set_color('lightgrey')
    ax.spines['bottom'].set_linewidth(0.5)

    # Aggiungi linee grigie chiare per ogni etichetta dell'asse delle ascisse
    ax.grid(axis='x', color='lightgrey', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # Posiziona le linee della griglia dietro le barre

    if fasce_basse is None:
        fasce_basse = []
    if fasce_alte is None:
        fasce_alte = []

    # Aggiungere delle linee verticali nere e in grassetto nei due valori delle fasce
    if cod_domanda != 'C4' and cod_domanda != 'C3':
        for i in range(len(fasce_basse)):
            ax.axvline(fasce_basse[i], color='#fe4254', linestyle='-', linewidth=1.5)
            ax.text(fasce_basse[i], 1.1, f"{fasce_basse[i]}%", ha='center', va='top', color='#fe4254', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    elif cod_domanda != 'C4' and cod_domanda == 'C3':
        for i in range(len(fasce_basse)):
            ax.axvline(fasce_basse[i], color='#fe4254', linestyle='-', linewidth=1.5)
            if i != 0:
                ax.text(fasce_basse[i] - 0.5, 1.1, f"{fasce_basse[i]}%", ha='center', va='top', color='#fe4254', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
            else:
                ax.text(fasce_basse[i], 1.1, f"{fasce_basse[i]}%", ha='center', va='top', color='#fe4254', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    else :
        for i in range(len(fasce_basse)):
            ax.axvline(100 - fasce_basse[i], color='#fe4254', linestyle='-', linewidth=1.5)
            ax.text(100 - fasce_basse[i], 1.1, f"{fasce_basse[i]}%", ha='center', va='top', color='#fe4254', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)

    if cod_domanda != 'C3':
        for i in range(len(fasce_alte)):
            ax.axvline(100 - fasce_alte[i], color='#005e34', linestyle='-', linewidth=1.5)
            ax.text(100 - fasce_alte[i], 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    else:
        for i in range(len(fasce_alte)):
            ax.axvline(100 - fasce_alte[i], color='#005e34', linestyle='-', linewidth=1.5)
            if i != 0:
                ax.text(100 - fasce_alte[i] + 0.8, 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
            else:
                ax.text(100 - fasce_alte[i], 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    # else:
    #     for i in range(len(fasce_alte)):
    #         ax.axvline(fasce_alte[i], color='#005e34', linestyle='-', linewidth=1.5)
    #         ax.text(fasce_alte[i], 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    # Adatta il layout del grafico
    fig.tight_layout()

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    fig.savefig(byte_io, format=format)
    plt.close(fig)
    #  Rimuove i bordi inutili
    plt.box(False)  

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()

def generate_barre_in_pila_serie_s(colors, sizes, fasce, format, width, height):
    """
    Genera un grafico a barre in pila con colori personalizzati e restituisce l'immagine come array di byte.

    Args:
        colors (list): Lista di colori in formato "rgb(r, g, b)".
        sizes (list): Dimensioni delle fette del grafico.

    Returns:
        bytearray: L'immagine del grafico a barre in pila come array di byte.
    """

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 10
        height = 3
    else:
        width = width / EMU
        height = height / EMU

    font_size = calcola_font_size(width, height)
    
    if not colors or not sizes or not fasce or sizes.count(0) == len(sizes): 
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

    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(width, height))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    # for i in range(len(normalized_sizes)):
    #     ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None, height=0.6)
    #     if normalized_sizes[i] != 0:
    #         ax.text(left + normalized_sizes[i] / 2, 0.4, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=12, fontweight='bold')
    #     left += normalized_sizes[i]
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None)
        if normalized_sizes[i] != 0 and i == 0:
            ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=font_size, fontweight='bold', fontproperties=avenir_font_path)
        left += normalized_sizes[i]

    # Personalizzazioni
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xticklabels([f"{i}%" for i in range(0, 101, 20)], fontproperties=avenir_font_path)
    ax.set_yticks([]) 

    # Aggiungi margine inferiore
    ax.margins(y=0.2)

    # Rimuovi i bordi del grafico
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    # Rendi l'asse delle ascisse più chiara
    ax.spines['bottom'].set_color('lightgrey')
    ax.spines['bottom'].set_linewidth(0.5)

    # Aggiungi linee grigie chiare per ogni etichetta dell'asse delle ascisse
    ax.grid(axis='x', color='lightgrey', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # Posiziona le linee della griglia dietro le barre

    # Aggiungere delle linee verticali nere e in grassetto nei due valori delle fasce
    for i in range(len(fasce)):
        ax.axvline(fasce[i], color='black', linestyle='-', linewidth=1.5)
        ax.text(fasce[i], 1.1, f"{fasce[i]}%", ha='center', va='top', color='black', fontsize=font_size, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)

    # Adatta il layout del grafico
    fig.tight_layout()

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    fig.savefig(byte_io, format=format)
    plt.close(fig)

    #  Rimuove i bordi inutili
    plt.box(False)  

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()
