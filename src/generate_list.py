from PIL import Image, ImageDraw, ImageFont
import io
import math
import textwrap


# def generate_list(items, format):
#     # controllo se la lista è vuota
#     if not items or len(items) == 0:
#         img = Image.new("RGB", (800, 50), "white")
#         draw = ImageDraw.Draw(img)
#         font = ImageFont.load_default()
#         img_byte_arr = io.BytesIO()
#         img.save(img_byte_arr, format=format)
#         img_byte_arr.seek(0)
#         return img_byte_arr
    
#     # Aggiungi righe vuote per arrivare a un minimo di 8 elementi
#     while len(items) < 8:
#         items.append({'Key': '', 'Value': 0})

        
#     # Divide items into two columns
#     if len(items) > 8:
#         mid_index = math.ceil(len(items) / 2)
#         left_items = items[:mid_index]
#         right_items = items[mid_index:]
#     else:
#         left_items = items
#         right_items = []  # Colonna destra vuota

#     # Generate list image
#     width, height = 800, 50 + max(len(left_items), len(right_items)) * 30  # Dimensioni dinamiche in base alla lista
#     img = Image.new("RGB", (width, height), "white")
#     draw = ImageDraw.Draw(img)

#     # Percorso del font Avenir (modifica se necessario)
#     font_path = "fonts/Figtree-VariableFont_wght.ttf"
    
#     try:
#         font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
#     except IOError:
#         font = ImageFont.load_default()  # Usa font di default se non trovato
#         print("Font Avenir non trovato, usando font di default.")

#     y = 20
#     for item in left_items:
#         k = item['Key']
#         v = item['Value']
#         v_rounded = math.ceil(v)

#         # Suddividi la chiave in più righe se è troppo lunga
#         wrapped_key = textwrap.wrap(k, width=30)
#         # Scrivi la chiave su più righe
#         for line in wrapped_key:
#             draw.text((20, y), line, fill="black", font=font)
#             y += 20  # Spaziatura tra le righe della chiave

#         # Scrivi il valore
#         if v_rounded != 0:
#             draw.text((300, y - 20), f"{v_rounded}%", fill="black", font=font)  # Allinea il valore all'ultima riga della chiave
#         y += 10  # Spaziatura tra gli elementi

#     y = 20
#     for item in right_items:
#         k = item['Key']
#         v = item['Value']
#         v_rounded = math.ceil(v)

#         # Suddividi la chiave in più righe se è troppo lunga
#         wrapped_key = textwrap.wrap(k, width=30)
#         # Scrivo la chiave
#         for line in wrapped_key:
#             draw.text((420, y), line, fill="black", font=font)
#             y += 20
#         # Scrivo il valore
#         if v_rounded != 0:
#             draw.text((700, y - 20), f"{v_rounded}%", fill="black", font=font)
#         y += 10

#     # Salva l'immagine in un buffer di memoria
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format=format)
#     img_byte_arr.seek(0)
    
#     return img_byte_arr

def generate_list(items, format, width, height):
    # Imposta dimensioni fisse
    if width is None or height is None or width == 0.0 or height == 0.0:
        width, height = 800, 400  # Altezza fissa
        # Impostazioni dinamiche in base al numero di items
    num_items = len(items) if items else 0
    if num_items > 16:
        max_items_per_column = math.ceil(num_items / 2)
        font_size = 12
        line_spacing = 12
        y_step = 3
    else:
        max_items_per_column = 8
        font_size = 16
        line_spacing = 15
        y_step = 5
    
    # Se la lista è vuota, restituisci un'immagine vuota
    if not items or len(items) == 0:
        img = Image.new("RGB", (width, height), "white")
        font_path = "fonts/Figtree-VariableFont_wght.ttf"
        try:
            font = ImageFont.truetype(font_path, 20)  # Carica font personalizzato
        except IOError:
            font = ImageFont.load_default()  # Usa font di default se non trovato
        draw = ImageDraw.Draw(img)
        draw.text((200, 150), "Nessun dato disponibile", fill="black", font=font, anchor='mm')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=format)
        img_byte_arr.seek(0)
        return img_byte_arr
    
    # Aggiungi elementi vuoti fino a 10 se necessario
    while len(items) < max_items_per_column:
        items.append({'Key': '', 'Value': 0})
    
    # Divide items in colonne (prima riempie la sinistra, poi la destra)
    left_items = items[:max_items_per_column]
    right_items = items[max_items_per_column:max_items_per_column*2]
    
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    
    # Percorso del font
    font_path = "fonts/Figtree-VariableFont_wght.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)  # Ridotto font per ottimizzare lo spazio
    except IOError:
        font = ImageFont.load_default()
    
    y_start = 5  # Margine superiore
    # y_step = 5  # Spaziatura verticale ridotta
    # line_spacing = 15  # Spaziatura ridotta tra le righe
    
    # Disegna la prima colonna
    y = y_start
    for item in left_items:
        k, v = item['Key'], math.ceil(item['Value'])
        wrapped_key = textwrap.wrap(k, width=25)  # Avvolge il testo con maggiore efficienza
        
        for line in wrapped_key:
            draw.text((20, y), line, fill="black", font=font)
            y += line_spacing
        
        if v != 0:
            draw.text((250, y - line_spacing), f"{v}%", fill="black", font=font)
        y += y_step
    
    # Disegna la seconda colonna
    y = y_start
    for item in right_items:
        k, v = item['Key'], math.ceil(item['Value'])
        wrapped_key = textwrap.wrap(k, width=25)  # Avvolge il testo con maggiore efficienza
        
        for line in wrapped_key:
            draw.text((300, y), line, fill="black", font=font)
            y += line_spacing
        
        if v != 0:
            draw.text((560, y - (len(wrapped_key) * line_spacing)), f"{v}%", fill="black", font=font)
        y += y_step
    
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