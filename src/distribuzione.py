import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from constants import EMU

# Importa il font manager di Matplotlib
from matplotlib import font_manager as fm


def create_survey_chart(dataArray, category_names, colors, format, color_labels, width, height, fasce_basse, fasce_alte, cod_domanda):
    """
    Crea un grafico a barre orizzontali a partire dai dati forniti.

    Parameters
    ----------
    data : dict
        Un dizionario che mappa le domande a una lista di valori.
        Si assume che tutte le liste abbiano la stessa lunghezza.
    category_names : list of str
        Le etichette delle categorie (es: Strongly disagree, Agree, ecc.).
    colors : list of str
        Una lista di colori per ogni categoria. 

    Returns
    -------
    img_bytes : bytes
        L'immagine del grafico sotto forma di byte.
    """

    font_path = "fonts/Figtree-Bold.ttf"
    avenir_font_path = fm.FontProperties(fname=font_path)

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 14
        height = 7
    else:
        width = width / EMU
        height = height / EMU

    if isinstance(dataArray, list) and all(isinstance(p, dict) and 'Dimensione' in p and 'Valori' in p for p in dataArray):
        data = {p['Dimensione']: p['Valori'] for p in dataArray}
    else:
        raise ValueError("dataArray deve essere una lista di dizionari con chiavi 'Dimensione' e 'Valori'.")

    if not colors or not data or not category_names or not color_labels or len(data) == 0: 
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

    labels = list(data.keys())
    values = np.array(list(data.values()))
    cumulative_values = values.cumsum(axis=1)

    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(width, height))  # Imposta la dimensione della figura per renderla più stretta in altezza
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, np.sum(values, axis=1).max())
    # Aggiungi il simbolo delle percentuali all'asse delle ascisse
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))

    # Imposta le etichette sull'asse delle y in grassetto
    ax.set_yticklabels(labels, fontweight='bold', fontsize=12, fontproperties=avenir_font_path)


    for i, (category, color) in enumerate(zip(category_names, colors)):
        widths = values[:, i]
        starts = cumulative_values[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label="Stress " + category, color=color)

        # Aggiungi etichette al centro di ogni barra
        ax.bar_label(rects, labels=[f'{w:.1f}%' if w != 0 else '' for w in widths], label_type='center', color=color_labels[i], fontsize=12, fontweight='bold', fontproperties=avenir_font_path)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, -0.2),
              loc='upper center', fontsize='small', frameon=False, prop=avenir_font_path)
    
    
    # Rimuovi il bordo esterno del grafico
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Aggiungi linee grigie chiare per ogni etichetta dell'asse delle ascisse
    ax.grid(axis='x', color='lightgrey', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # Posiziona le linee della griglia dietro le barre

    # aggiungi una riga rossa sopra il grafico a partire all'80% dell'asse x
    if (not fasce_basse or not fasce_alte) and cod_domanda != 'C4':
        ax.axvline(x=80, color='red', linestyle='-', linewidth=2)
        # Aggiungi un'etichetta sopra la linea rossa
        ax.text(77, -0.8, '% rilevante \nStress alto', color='black', fontsize=12, fontweight='bold', fontproperties=avenir_font_path)
    else:
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

        if cod_domanda != 'C3' and cod_domanda != 'C4':
            for i in range(len(fasce_alte)):
                ax.axvline(100 - fasce_alte[i], color='#005e34', linestyle='-', linewidth=1.5)
                ax.text(100 - fasce_alte[i], 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
        elif cod_domanda != 'C4':
            for i in range(len(fasce_alte)):
                ax.axvline(100 - fasce_alte[i], color='#005e34', linestyle='-', linewidth=1.5)
                if i != 0:
                    ax.text(100 - fasce_alte[i] + 0.8, 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
                else:
                    ax.text(100 - fasce_alte[i], 1.1, f"{fasce_alte[i]}%", ha='center', va='top', color='#005e34', fontsize=10, fontweight='bold', transform=ax.get_xaxis_transform(), fontproperties=avenir_font_path)
    
    # Salvataggio e visualizzazione
    fig.tight_layout()

    # Salva l'immagine in un buffer
    byte_io = io.BytesIO()
    fig.savefig(byte_io, format=format)
    plt.close(fig) 
    byte_io.seek(0)

    return byte_io.read()
