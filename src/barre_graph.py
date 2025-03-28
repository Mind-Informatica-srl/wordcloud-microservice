import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from matplotlib import font_manager as fm

def generate_barre_in_pila(colors, labels, sizes, format):
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

    if not colors or not sizes or not labels or sizes.count(0) == len(sizes): 
        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(800, 600))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            dwg.write(byte_io)
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
        
    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(10, 3))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    # for i in range(len(normalized_sizes)):
    #     ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None, height=0.6)
    #     if normalized_sizes[i] != 0:
    #         ax.text(left + normalized_sizes[i] / 2, 0.4, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=12, fontweight='bold')
    #     left += normalized_sizes[i]
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None)
        if normalized_sizes[i] != 0:
            ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=10, fontweight='bold', fontproperties=avenir_font_path)
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

    # Adatta il layout del grafico
    plt.tight_layout()

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format=format)
    plt.close()

    #  Rimuove i bordi inutili
    plt.box(False)  

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()

def generate_barre_in_pila_serie_s(colors, sizes, fasce, format):
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

    if not colors or not sizes or not fasce or sizes.count(0) == len(sizes): 
        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(800, 600))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            dwg.write(byte_io)
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

    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(10, 3))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    # for i in range(len(normalized_sizes)):
    #     ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None, height=0.6)
    #     if normalized_sizes[i] != 0:
    #         ax.text(left + normalized_sizes[i] / 2, 0.4, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=12, fontweight='bold')
    #     left += normalized_sizes[i]
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None)
        if normalized_sizes[i] != 0 and i == 0:
            ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='bottom', color='black', fontsize=10, fontweight='bold', fontproperties=avenir_font_path)
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
        ax.text(fasce[i], 1.1, f"{fasce[i]}%", ha='center', va='top', color='black', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)

    # Adatta il layout del grafico
    plt.tight_layout()

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format=format)
    plt.close()

    #  Rimuove i bordi inutili
    plt.box(False)  

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()
