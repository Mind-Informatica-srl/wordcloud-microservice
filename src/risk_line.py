import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np

def create_risk_line_chart(categories, values, risk_zones, risk_colors, legend_labels):
    """
    Crea un grafico a linea con fasce di rischio sullo sfondo.

    :param categories: Lista di stringhe, nomi delle categorie (asse X).
    :param values: Lista di valori corrispondenti a ogni categoria.
    :param risk_zones: Lista di tuple, ogni tuple rappresenta (inizio, fine) per una fascia di rischio.
    :param risk_colors: Lista di stringhe, colori delle fasce di rischio.
    :param legend_labels: Lista di stringhe, etichette della leggenda delle fasce di rischio.
    """
    x_positions = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(14, 7))

    # Aggiungi le fasce di rischio come sfondo
    risk_patches = []
    for i, (start, end) in enumerate(risk_zones):
        patch = ax.axhspan(start, end, color=risk_colors[i], alpha=0.8, label=f"Rischio: {legend_labels[i]}")
        risk_patches.append(patch)

    # Disegna la linea
    ax.plot(x_positions, values, color="black", linewidth=2)

    # Aggiungi i valori sopra i punti
    for x, y in zip(x_positions, values):
        ax.text(x, y + 3, f"{y:.2f}", ha="center", fontsize=10, color="black")

    # Configura assi e legenda
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.set_ylim(0, max(risk_zones[-1]) + 10)
    # Aggiungi la legenda per le fasce di rischio lateralmente al grafico
    ax.legend(handles=risk_patches, loc="center left", bbox_to_anchor=(1, 0.5), title="Fasce di Rischio", title_fontsize="medium", frameon=False)

    # Rimuovi il bordo nero intorno all'area del grafico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Mostra il grafico
    plt.tight_layout()

    byte_io = io.BytesIO()
    plt.savefig(byte_io, format='svg')
    plt.close()

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