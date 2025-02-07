import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

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

    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(10, 3))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None, label=f"{labels[i]}: {normalized_sizes[i]:.2f}%")
        ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='center', color='black', fontsize=12)
        left += normalized_sizes[i]

    # Personalizzazioni
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xticklabels([f"{i}%" for i in range(0, 101, 20)])
    ax.set_yticks([]) 

    # Aggiungi margine inferiore
    ax.margins(y=0.2)

    # Aggiungi la legenda sotto l'asse delle x
    ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(labels), frameon=False)


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

def generate_barre_in_pila_serie_s(colors, sizes, format):
    """
    Genera un grafico a barre in pila con colori personalizzati e restituisce l'immagine come array di byte.

    Args:
        colors (list): Lista di colori in formato "rgb(r, g, b)".
        sizes (list): Dimensioni delle fette del grafico.

    Returns:
        bytearray: L'immagine del grafico a barre in pila come array di byte.
    """

    # Calcola la somma delle dimensioni per normalizzare le percentuali
    total = sum(sizes)
    normalized_sizes = [size / total * 100 for size in sizes]

    # Crea il grafico a barre in pila
    fig, ax = plt.subplots(figsize=(10, 3))  # Imposta la dimensione della figura per renderla più stretta in altezza
    left = 0
    for i in range(len(normalized_sizes)):
        ax.barh([''], normalized_sizes[i], left=left, color=colors[i], edgecolor=None)
        if i == 0:
            ax.text(left + normalized_sizes[i] / 2, 0, f"{normalized_sizes[i]:.2f}%", ha='center', va='center', color='black', fontsize=12)
        left += normalized_sizes[i]

    # Personalizzazioni
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xticklabels([f"{i}%" for i in range(0, 101, 20)])
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
