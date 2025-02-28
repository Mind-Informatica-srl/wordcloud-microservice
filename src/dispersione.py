import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text
import io
import textwrap
import matplotlib.patches as patches

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
    if not x or not y or not labels: 
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_axis_off()
        ax.text(0.5, 0.5, 'Dati Mancanti', horizontalalignment='center', verticalalignment='center', fontsize=20, color='red', transform=ax.transAxes)
        plt.tight_layout()
        byte_io = io.BytesIO()
        plt.savefig(byte_io, format=format)
        plt.close()
        byte_io.seek(0)
        return byte_io.read()
    # Creazione del grafico
    fig, ax = plt.subplots(figsize=(14, 7))

    # Aggiunta dei punti
    ax.scatter(x, y, color='red')
    # Aggiunta delle etichette ai punti
    metaX = 50
    metaY = 50
    texts = []
    for i, label in enumerate(labels):
        wrapped_label = "\n".join(textwrap.wrap(label, width=30))
        # Impedisce che l'etichetta esca dai margini superiori o inferiori
        y_text = min(max(y[i] + 0.05, 1), 97)
        # Impedisce che l'etichetta esca dai margini laterali
        x_text = min(max(x[i] + 0.05, 11), 90)
        if x[i] > metaX and y[i] > metaY:
            alignment = {'verticalalignment': 'bottom', 'horizontalalignment': 'left'}
        elif x[i] > metaX and y[i] <= metaY:
            alignment = {'verticalalignment': 'top', 'horizontalalignment': 'left'}
        elif x[i] <= metaX and y[i] > metaY:
            alignment = {'verticalalignment': 'bottom', 'horizontalalignment': 'right'}
        else:
            alignment = {'verticalalignment': 'top', 'horizontalalignment': 'right'}
        
        texts.append(ax.text(x_text, y_text, wrapped_label, fontsize=8, **alignment))


    # Se nell'intorno del punto ci sono altre etichette, le sposta per evitare sovrapposizioni
    adjust_text(
        texts, 
        ax=ax,
        expand_text=(1.1, 1.1),
        force_points=0.5,
        only_move={'text':'xy'}
    )

    # Aggiunta delle linee per dividere il grafico in 4 parti uguali
    ax.axhline(y= metaY, color='lightgrey', linestyle='-', zorder=0)
    ax.axvline(x= metaX, color='lightgrey', linestyle='-', zorder=0)

    # Aggiungere su ogni riquadro creato un'etichetta, se il riquadro è in basso si mette sulla base
    # se è in alto si mette sopra
    # Etichette per i quadranti
    quartoquadrante = 12.5
    primoquarto = quartoquadrante
    terzoquarto = 65
    ax.text(primoquarto, 102, "A. NON IMPORTANTI E SCELTE DA MOLTI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    ax.text(terzoquarto, 102, "B. IMPORTANTI E SCELTE DA MOLTI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    # Aggiungi un cerchio rosso sopra l'etichetta
    circle = patches.Ellipse((75, 102.5), width=25,height=6, edgecolor='red', facecolor='none', linewidth=2, zorder=10, clip_on=False)
    ax.add_patch(circle)
    ax.text(primoquarto, -1, "C. NON IMPORTANTI E SCELTE DA POCHI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')
    ax.text(terzoquarto, -1, "D. IMPORTANTI E SCELTE DA POCHI", fontsize=10, fontweight='bold', backgroundcolor='darkgreen', color='white')



    # Personalizzazioni
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 102)
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
