import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import svgwrite

def create_risk_bar_chart(categories, values, groups, risk_zones, risk_colors, legend_labels, bar_colors, format):
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
    if not categories or not values or not groups or not risk_zones or not risk_colors or not legend_labels or not bar_colors or len(values) == 0 or all(value == 0 for value in values): 
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

    try:
        num_categories = len(categories)
        bar_height = 0.1 # / len(groups)
        fig, ax = plt.subplots(figsize=(14, 7)) 

        # Aggiungi le fasce di rischio come sfondo
        risk_patches = []
        for i, (start, end) in enumerate(risk_zones):
            patch = ax.axvspan(start, end, color=risk_colors[i], alpha=0.8, label=f"Rischio: {legend_labels[i]}")
            risk_patches.append(patch)

        # Definizione delle posizioni per le barre
        y_positions = np.arange(num_categories)

        bar_col = []
        for i in range(len(groups)):
            bar_col.append(bar_colors[i])

        bc = reversed(bar_col)
        bc = list(bc)
        
        group_patches = []
        for i, group in enumerate(groups):
            bar = ax.barh(
                y_positions + i * bar_height,
                [val[i] for val in values],
                height=bar_height,
                label=group,
                color=bc[i]
            )
            group_patches.append(bar)

            # Aggiungi i valori all'estremo destro delle barre
            for j, val in enumerate(values):
                ax.text(val[i], y_positions[j] + i * bar_height, f'{val[i]:.2f}', va='center', ha='left', fontsize=8, color='black', fontweight='bold')


        # Configura assi e legenda
        ax.set_yticks(y_positions + bar_height * (len(groups) - 1) / 2)
        ax.set_yticklabels(categories, fontsize=10, fontweight='bold')
        # Prima legenda per le fasce di rischio
        risk_legend = ax.legend(
            handles=risk_patches, 
            loc="upper center", 
            bbox_to_anchor=(0.5, -0.15), 
            ncol=len(risk_patches), 
            title="Fasce di Rischio", 
            frameon=False, 
            title_fontsize='medium'
        )    
        ax.add_artist(risk_legend)

        # Seconda legenda per i gruppi
        bar_colors_used = [bar_colors[groups.index(group)] for group in groups[::-1]]  # Inverti l'ordine dei colori
        group_legend = ax.legend(
            handles=[plt.Line2D([0], [0], color=color, lw=4) for color in reversed(bar_colors_used)], 
            labels=list(groups),  # Usa groups per le etichette della legenda in ordine inverso
            loc="center left", 
            bbox_to_anchor=(1, 0.5), 
            frameon=False  # Rimuovi il bordo
        )      
        ax.add_artist(group_legend)

        # Rimuovi il bordo nero intorno all'area del grafico
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Aggiungi spazio extra intorno al grafico
        plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.3)

        # Mostra il grafico
        plt.tight_layout()
        byte_io = io.BytesIO()
        plt.savefig(byte_io, format=format, bbox_extra_artists=(risk_legend, group_legend), bbox_inches='tight', dpi=300)
        plt.close()

        # Restituisce l'immagine come array di byte
        byte_io.seek(0)
        return byte_io.read()
    except Exception as e:
        print(f"Errore durante la creazione del grafico: {e}")
        return None