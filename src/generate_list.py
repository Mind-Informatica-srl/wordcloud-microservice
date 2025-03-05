from PIL import Image, ImageDraw, ImageFont
import io
import math


def generate_list(items, format):
    # Divide items into two columns
    mid_index = math.ceil(len(items) / 2)
    left_items = items[:mid_index]
    right_items = items[mid_index:]

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
        draw.text((20, y), f"{k}   {v_rounded}%", fill="black", font=font)
        y += 30

    y = 20
    for item in right_items:
        k = item['Key']
        v = item['Value']
        v_rounded = math.ceil(v)
        draw.text((420, y), f"{k}   {v_rounded}%", fill="black", font=font)
        y += 30

    # Salva l'immagine in un buffer di memoria
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    
    return img_byte_arr