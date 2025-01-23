import numpy as np
import matplotlib.pyplot as plt
import io


def create_survey_chart(data, category_names, colors=None, figsize=(9.2, 5)):
    """
    Crea un grafico a barre orizzontali a partire dai dati forniti.

    Parameters
    ----------
    data : dict
        Un dizionario che mappa le domande a una lista di valori.
        Si assume che tutte le liste abbiano la stessa lunghezza.
    category_names : list of str
        Le etichette delle categorie (es: Strongly disagree, Agree, ecc.).
    colors : list of str or None, optional
        Una lista di colori per ogni categoria. Se None, verrà usata la colormap di default.
    figsize : tuple of float, optional
        La dimensione della figura (default: (9.2, 5)).

    Returns
    -------
    img_bytes : bytes
        L'immagine del grafico sotto forma di byte.
    """
    labels = list(data.keys())
    values = np.array(list(data.values()))
    cumulative_values = values.cumsum(axis=1)

    # Usa i colori forniti o la colormap di default
    if colors is None:
        colors = plt.colormaps['RdYlGn'](np.linspace(0.15, 0.85, values.shape[1]))

    # Creazione del grafico
    fig, ax = plt.subplots(figsize=figsize)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(values, axis=1).max())

    for i, (category, color) in enumerate(zip(category_names, colors)):
        widths = values[:, i]
        starts = cumulative_values[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=category, color=color)

        # Calcola il colore del testo (chiaro o scuro)
        r, g, b, _ = color if isinstance(color, tuple) else plt.colors.to_rgba(color)
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    # Salva l'immagine in un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)  # Chiude il grafico per liberare memoria
    buffer.seek(0)
    img_bytes = buffer.getvalue()
    buffer.close()

    return img_bytes
