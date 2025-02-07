import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text
import io
import textwrap

# Dati
x = [1, 2, 1.5, 3, 2.5, 4, 4.5, 5, 2, 1, 1.2, 3.8, 4.2, 1.3, 0.8]  # Importanza
y = [0.5, 1, 1.5, 1.8, 2.5, 2.8, 3.5, 4, 1.2, 1.8, 0.7, 3.2, 3.8, 0.9, 0.4]  # Frequenza di scelta
labels = [
    "Utilità del lavoro", "Senso di appartenenza", "Rapporto con l'Azienda", 
    "Ambiente di lavoro", "Orario di lavoro", "Quantità di lavoro",
    "Pianificazione del lavoro", "Prospettive di carriera", "Relazioni colleghi",
    "Autonomia e responsabilità inadeguate", "Identificazione Luxury", 
    "Cultura organizzativa", "Equilibrio tra lavoro e vita privata", 
    "Scarsa chiarezza dei ruoli", "Valutazione"
]
def generate_dispersione(x, y, labels, format):
    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(16, 8))

    # Aggiunta dei punti
    ax.scatter(x, y, color='red')
    # Aggiunta delle etichette ai punti
    texts = []
    for i, label in enumerate(labels):
        wrapped_label = "\n".join(textwrap.wrap(label, width=30))
        texts.append(ax.text(x[i], y[i] + 0.05, wrapped_label, fontsize=8, verticalalignment='bottom', horizontalalignment='left'))

    # Aggiustamento delle etichette per evitare sovrapposizioni
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey'))


    # Aggiunta delle linee per dividere il grafico in 4 parti uguali
    ax.axhline(y=(min(y) + max(y)) / 2, color='lightgrey', linestyle='-', zorder=0)
    ax.axvline(x=(min(x) + max(x)) / 2, color='lightgrey', linestyle='-', zorder=0)

    # Aggiungere su ogni riquadro creato un'etichetta, se il riquadro è in basso si mette sulla base
    # se è in alto si mette sopra
    # Etichette per i quadranti
    ax.text(20, max(y) + 1, "A. NON IMPORTANTI E SCELTE DA MOLTI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    ax.text(62.5, max(y) + 1, "B. IMPORTANTI E SCELTE DA MOLTI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    ax.text(20, 0, "C. NON IMPORTANTI E SCELTE DA POCHI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    ax.text(62.5, 0, "D. IMPORTANTI E SCELTE DA POCHI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')



    # Personalizzazioni
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(y) - 1, max(y) + 1)
    ax.set_xlabel("IMPORTANZA", fontsize=12, labelpad=10)
    ax.set_ylabel("FREQUENZA DI SCELTA", fontsize=12, labelpad=10)
    ax.spines['top'].set_color('green')
    ax.spines['right'].set_color('green')
    ax.spines['left'].set_color('green')
    ax.spines['bottom'].set_color('green')
    ax.tick_params(axis='both', which='both', color='green')

    # Imposta il colore del contorno a verde
    for spine in plt.gca().spines.values():
        spine.set_edgecolor('green')

    # Rimuovi le etichette degli assi
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])

    # Titolo
    # plt.title("Distribuzione Importanza-Frequenza", fontsize=14, pad=15)

    # Salvataggio e visualizzazione
    plt.tight_layout()

    byte_io = io.BytesIO()
    plt.savefig(byte_io, format=format)
    plt.close()

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()