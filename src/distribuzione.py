import numpy as np
import matplotlib.pyplot as plt
import io


def create_survey_chart(data, category_names, colors):
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
    labels = list(data.keys())
    values = np.array(list(data.values()))
    cumulative_values = values.cumsum(axis=1)

    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(14,7))
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, np.sum(values, axis=1).max())

    for i, (category, color) in enumerate(zip(category_names, colors)):
        widths = values[:, i]
        starts = cumulative_values[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=category, color=color)

        # Aggiungi etichette al centro di ogni barra
        ax.bar_label(rects, labels=[f'{w:.1f}%' if w != 0 else '' for w in widths], label_type='center', color="black", fontsize=10)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0.5, -0.2),
              loc='upper center', fontsize='small')
    
    
    # Rimuovi il bordo esterno del grafico
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Aggiungi linee grigie chiare per ogni etichetta dell'asse delle ascisse
    ax.grid(axis='x', color='lightgrey', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # Posiziona le linee della griglia dietro le barre
    
    # Salvataggio e visualizzazione
    plt.tight_layout()

    # Salva l'immagine in un buffer
    byte_io = io.BytesIO()
    plt.savefig(byte_io, format='svg')
    plt.close() 
    byte_io.seek(0)

    return byte_io.read()
