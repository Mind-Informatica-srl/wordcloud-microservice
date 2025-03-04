import sys
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from PIL import Image
import svgwrite

def generate_wordcloud(word_colors, word_frequencies, default_color, format):
    """
    Genera una word cloud con colori e frequenze personalizzate e restituisce l'immagine come array di byte.

    Args:
        word_colors (dict): Mappa di parole e i loro colori in formato "rgb(r, g, b)".
        word_frequencies (dict): Mappa di parole e le loro frequenze.
        default_color (str): Colore predefinito per le parole mancanti nella mappa.

    Returns:
        bytearray: L'immagine della word cloud come array di byte.
    """
    if not word_colors or not word_frequencies or not default_color or word_frequencies == {} or all(value == 0 for value in word_frequencies.values()):

        # Genera un'immagine bianca
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
            byte_io = io.BytesIO()
            img.save(byte_io, format=format)
            byte_io.seek(0)
            return byte_io.read()
    
    # Funzione per applicare i colori personalizzati
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return word_colors.get(word, default_color)

    # Crea la word cloud
    font_path = "fonts/Figtree-VariableFont_wght.ttf"
    wc = WordCloud(width=800, height=400, background_color="white", font_path=font_path).generate_from_frequencies(word_frequencies)

    # Applica i colori personalizzati
    wc.recolor(color_func=custom_color_func)

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    wc.to_image().save(byte_io, format=format)

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()

if __name__ == "__main__":
    # Carica i parametri dalla riga di comando
    word_colors = json.loads(sys.argv[1])
    word_frequencies = json.loads(sys.argv[2])
    default_color = sys.argv[3]