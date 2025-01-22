import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np

def create_risk_bar_chart(categories, values, groups, risk_zones, risk_colors, legend_labels, bar_colors):
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

    try:
        num_categories = len(categories)
        bar_height = 0.1 / len(groups)
        fig, ax = plt.subplots(figsize=(16, 8)) 

        # Aggiungi le fasce di rischio come sfondo
        risk_patches = []
        for i, (start, end) in enumerate(risk_zones):
            patch = ax.axvspan(start, end, color=risk_colors[i], label=f"Rischio: {legend_labels[i]}")
            risk_patches.append(patch)

        # Definizione delle posizioni per le barre
        y_positions = np.arange(num_categories)
        group_patches = []
        for i, group in enumerate(groups):
            bar = ax.barh(
                y_positions + i * bar_height,
                [val[i] for val in values],
                height=bar_height,
                label=group,
                color=bar_colors[i]
            )
            group_patches.append(bar)

        # Configura assi e legenda
        ax.set_yticks(y_positions + bar_height * (len(groups) - 1) / 2)
        ax.set_yticklabels(categories)
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
        group_legend = ax.legend(
            handles=[plt.Line2D([0], [0], color=color, lw=4) for color in bar_colors], 
            labels=groups,  # Usa groups per le etichette della legenda
            loc="center left", 
            bbox_to_anchor=(1, 0.5), 
            frameon=False  # Rimuovi il bordo
        )      
        ax.add_artist(group_legend)
        ax.grid(axis="x", linestyle="--", alpha=0.5)

        # Rimuovi il bordo nero intorno all'area del grafico
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Aggiungi spazio extra intorno al grafico
        plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.3)

        # Mostra il grafico
        plt.tight_layout()
        byte_io = io.BytesIO()
        plt.savefig(byte_io, format='PNG', bbox_extra_artists=(risk_legend, group_legend), bbox_inches='tight')
        plt.close()

        # Restituisce l'immagine come array di byte
        byte_io.seek(0)
        return byte_io.read()
    except Exception as e:
        print(f"Errore durante la creazione del grafico: {e}")
        return None