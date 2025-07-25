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

def create_risk_bar_chart(categories, values, groups, risk_zones, risk_colors, legend_labels, legend_colors, bar_colors, format, width, height):
    """
    Crea un grafico a barre orizzontali con fasce di rischio sullo sfondo.

    :param categories: Lista di stringhe, nomi delle categorie.
    :param values: Lista di liste, ogni sottolista rappresenta i valori di un gruppo per categoria.
    :param groups: Lista di stringhe, nomi dei gruppi.
    :param risk_zones: Lista di tuple, ogni tuple rappresenta (inizio, fine) per una fascia di rischio.
    :param risk_colors: Lista di stringhe, colori delle fasce di rischio.
    :param legend_labels: Lista di stringhe, etichette della leggenda.
    :param bar_colors: Lista di stringhe, colori delle barre per i gruppi.
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
    
    if not categories or not values or not groups or not risk_zones or not risk_colors or not legend_labels or not bar_colors or len(values) == 0 or all(value == 0 for value in values): 
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

    try:
        num_categories = len(categories)
        bar_height = 0.30 # / len(groups)
        bar_spacing = 0.10
        fig, ax = plt.subplots(figsize=(width, height)) 

        # Aggiungi le fasce di rischio come sfondo
        risk_patches = []
        for i, (start, end) in enumerate(risk_zones):
            patch = ax.axvspan(start, end, color=risk_colors[i], alpha=1, label=f"Rischio: {legend_labels[i]}")
            risk_patches.append(patch)

        # Definizione delle posizioni per le barre
        y_positions = np.arange(num_categories) * (len(groups) * (bar_height + bar_spacing) + 0.2)

        bar_col = []
        for i in range(len(groups)):
            bar_col.append(bar_colors[i])

        bc = reversed(bar_col)
        bc = list(bc)
        
        group_patches = []
        for i, group in enumerate(groups):
            bar = ax.barh(
                y_positions + i * (bar_height + bar_spacing),
                [val[i] for val in values],
                height=bar_height,
                label=group,
                color=bc[i]
            )
            group_patches.append(bar)

            # Aggiungi i valori all'estremo destro delle barre
            for j, val in enumerate(values):
                if val[i] != 0 and val[i] != None and val[i] != 0.00:
                    ax.text(val[i], y_positions[j] + i * (bar_height + bar_spacing), f'{val[i]:.2f}', va='center', ha='left', fontsize=font_size, color='black', fontweight='bold', fontproperties=avenir_font_path)


        # Configura assi e legenda
        ax.set_yticks(y_positions + bar_height * (len(groups) - 1) / 2)
        ax.set_yticklabels(categories, fontsize=font_size, fontweight='bold', fontproperties=avenir_font_path)
        # Prima legenda per le fasce di rischio
        risk_legend = ax.legend(
            handles=risk_patches, 
            loc="upper center", 
            bbox_to_anchor=(0.5, -0.15), 
            ncol=len(risk_patches), 
            title="Fasce di Rischio", 
            frameon=False, 
            title_fontsize='medium',
            prop= avenir_font_path
        )    
        ax.add_artist(risk_legend)

        # Seconda legenda per i gruppi
        bar_colors_used = [bar_colors[groups.index(group)] for group in groups[::-1]]  # Inverti l'ordine dei colori
        group_legend = ax.legend(
            handles=[plt.Line2D([0], [0], color=color, lw=4) for color in reversed(bar_colors_used)], 
            labels=list(groups),  # Usa groups per le etichette della legenda in ordine inverso
            loc="center left", 
            bbox_to_anchor=(1, 0.5), 
            frameon=False,  # Rimuovi il bordo
            prop=avenir_font_path,
            fontsize=font_size,
        )      
        for text, color in zip(group_legend.get_texts(), legend_colors):
            if color != "" and color != None:
                text.set_color(color)
            else:
                text.set_color("black")
        ax.add_artist(group_legend)

        # Rimuovi il bordo nero intorno all'area del grafico
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Aggiungi spazio extra intorno al grafico
        fig.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.3)

        # Mostra il grafico
        fig.tight_layout()
        byte_io = io.BytesIO()
        fig.savefig(byte_io, format=format, bbox_extra_artists=(risk_legend, group_legend), bbox_inches='tight', dpi=300)
        plt.close(fig)

        # Restituisce l'immagine come array di byte
        byte_io.seek(0)
        return byte_io.read()
    except Exception as e:
        print(f"Errore durante la creazione del grafico: {e}")
        return None