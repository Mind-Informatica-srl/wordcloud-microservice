from PIL import Image, ImageDraw, ImageFont
import io
import math
import textwrap


def generate_list(items, format):
    # controllo se la lista è vuota
    if not items or len(items) == 0:
        img = Image.new("RGB", (800, 50), "white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=format)
        img_byte_arr.seek(0)
        return img_byte_arr
    
    # Aggiungi righe vuote per arrivare a un minimo di 8 elementi
    while len(items) < 8:
        items.append({'Key': '', 'Value': 0})

        
    # Divide items into two columns
    if len(items) > 8:
        mid_index = math.ceil(len(items) / 2)
        left_items = items[:mid_index]
        right_items = items[mid_index:]
    else:
        left_items = items
        right_items = []  # Colonna destra vuota

    # Generate list image
    width, height = 800, 50 + max(len(left_items), len(right_items)) * 30  # Dimensioni dinamiche in base alla lista
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Percorso del font Avenir (modifica se necessario)
    font_path = "fonts/Figtree-VariableFont_wght.ttf"
    
    try:
        font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
    except IOError:
        font = ImageFont.load_default()  # Usa font di default se non trovato
        print("Font Avenir non trovato, usando font di default.")

    y = 20
    for item in left_items:
        k = item['Key']
        v = item['Value']
        v_rounded = math.ceil(v)

        # Suddividi la chiave in più righe se è troppo lunga
        wrapped_key = textwrap.wrap(k, width=30)
        # Scrivi la chiave su più righe
        for line in wrapped_key:
            draw.text((20, y), line, fill="black", font=font)
            y += 20  # Spaziatura tra le righe della chiave

        # Scrivi il valore
        if v_rounded != 0:
            draw.text((300, y - 20), f"{v_rounded}%", fill="black", font=font)  # Allinea il valore all'ultima riga della chiave
        y += 10  # Spaziatura tra gli elementi

    y = 20
    for item in right_items:
        k = item['Key']
        v = item['Value']
        v_rounded = math.ceil(v)

        # Suddividi la chiave in più righe se è troppo lunga
        wrapped_key = textwrap.wrap(k, width=30)
        # Scrivo la chiave
        for line in wrapped_key:
            draw.text((420, y), line, fill="black", font=font)
            y += 20
        # Scrivo il valore
        if v_rounded != 0:
            draw.text((700, y - 20), f"{v_rounded}%", fill="black", font=font)
        y += 10

    # Salva l'immagine in un buffer di memoria
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    
    return img_byte_arr

def generate_fonti_list(items, format):
    # controllo se la lista è vuota
    if not items or len(items) == 0:
        img = Image.new("RGB", (800, 50), "white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=format)
        img_byte_arr.seek(0)
        return img_byte_arr

    # Generate list image
    width, height = 800, 50 + len(items) * 30  # Dimensioni dinamiche in base alla lista
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Percorso del font Avenir (modifica se necessario)
    font_path = "fonts/Figtree-VariableFont_wght.ttf"
    
    try:
        font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
    except IOError:
        font = ImageFont.load_default()  # Usa font di default se non trovato
        print("Font Avenir non trovato, usando font di default.")

    y = 20
    for item in items:
        k = item['Key']
        draw.text((20, y), f"{k}", fill="black", font=font)
        y += 30

    # Salva l'immagine in un buffer di memoria
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    
    return img_byte_arr