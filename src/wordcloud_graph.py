import sys
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from constants import EMU

def generate_wordcloud(word_colors, word_frequencies, default_color, format, width, height):
    """
    Genera una word cloud con colori e frequenze personalizzate e restituisce l'immagine come array di byte.

    Args:
        word_colors (dict): Mappa di parole e i loro colori in formato "rgb(r, g, b)".
        word_frequencies (dict): Mappa di parole e le loro frequenze.
        default_color (str): Colore predefinito per le parole mancanti nella mappa.

    Returns:
        bytearray: L'immagine della word cloud come array di byte.
    """

    if width is None or height is None or width == 0.0 or height == 0.0:
        width = 610
        height = 180
    else:
        pol_width = width / EMU
        pol_height = height / EMU
        width = int(pol_width * 100)
        height = int(pol_height * 100)

    if not word_colors or not word_frequencies or not default_color or word_frequencies == {} or all(value == 0 for value in word_frequencies.values()):

        # Genera un'immagine bianca
        if format.lower() == 'svg':
            # Genera un'immagine SVG bianca con una scritta in rosso
            dwg = svgwrite.Drawing(size=(610, 180))
            dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
            byte_io = io.BytesIO()
            byte_io.write(dwg.tostring().encode('utf-8'))
            byte_io.seek(0)
            return byte_io.read()
        else:
            img = Image.new('RGB', (610, 180), color='white')
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
    
    # Funzione per applicare i colori personalizzati
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return word_colors.get(word, default_color)

    # Crea la word cloud
    font_path = "fonts/Figtree-VariableFont_wght.ttf"
    wc = WordCloud(width=width, height=height, background_color=None, mode='RGBA', relative_scaling=0.6, font_path=font_path, prefer_horizontal=1).generate_from_frequencies(word_frequencies)

    # Applica i colori personalizzati
    wc.recolor(color_func=custom_color_func)

    # Salva l'immagine in un buffer di memoria
    byte_io = io.BytesIO()
    if format.lower() == 'svg':
        # layout = wc.layout_
        # dwg = svgwrite.Drawing(size=(width, height))
        # for word, font_size, position, orientation, color in layout:
        #     # Calcola la posizione e il colore
        #     x = position[0]
        #     y = position[1]
        #     color = custom_color_func(word[0], font_size, position, orientation)
        #     # Aggiungi il testo all'immagine SVG
        #     dwg.add(dwg.text(word[0], insert=(x, y), font_size=font_size, fill=color, font_family="Avenir"))
        # # Salva come SVG
        # byte_io.write(dwg.tostring().encode('utf-8'))
        byte_io.write(wc.to_svg(embed_font=True, optimize_embedded_font=True).encode('utf-8'))
    else:
        wc.to_image().save(byte_io, format=format)

    # Restituisce l'immagine come array di byte
    byte_io.seek(0)
    return byte_io.read()

if __name__ == "__main__":
    # Carica i parametri dalla riga di comando
    word_colors = json.loads(sys.argv[1])
    word_frequencies = json.loads(sys.argv[2])
    default_color = sys.argv[3]