from pptx import Presentation
import docx
from docx.shared import Inches
import os
import requests
import shutil
import io

def replace_text_in_pptx(ppt, replacements, image_replacements):
    # Sostituire i testi nei segnaposto
    for slide in ppt.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        for placeholder, text in replacements.items():
                            if placeholder in run.text:
                                run.text = run.text.replace(placeholder, text)

    # Sostituire le immagini
    for slide in ppt.slides:
        for shape in slide.shapes:
            if shape.shape_type == 13:  # 13 è il tipo per l'immagine
                image_element = shape._element

                # Cerca il testo alternativo nell'elemento XML (se presente)
                alt_text = None
                if image_element is not None:
                    # Cerca il testo alternativo all'interno dell'elemento XML
                    cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                    if cNvPr is not None:
                        alt_text = cNvPr.get('descr')

                for placeholder, image_path in image_replacements.items():
                    if placeholder in shape.image.filename:
                        # Posizione e dimensioni dell'immagine
                        left, top, width, height = shape.left, shape.top, shape.width, shape.height
                        # Aggiungere la nuova immagine
                        slide.shapes.add_picture(image_path, left, top, width, height)
                    elif alt_text is not None and placeholder in alt_text:
                        # Posizione e dimensioni dell'immagine
                        left, top, width, height = shape.left, shape.top, shape.width, shape.height
                        # Aggiungere la nuova immagine
                        slide.shapes.add_picture(image_path, left, top, width, height)
                        # Rimuove l'immagine originale
                        sp = shape
                        slide.shapes._spTree.remove(sp._element)


    # Salvare il file PPTX modificato
    storage_path = os.path.join("storage", "modificati")
    os.makedirs(storage_path, exist_ok=True)
    modified_pptx_path = os.path.join("storage", "modificati", "modified_pptx.pptx")
    ppt.save(modified_pptx_path)
    print(f"File PPTX modificato e salvato come '{modified_pptx_path}'")
    # Restituire i byte del file PPTX modificato
    with open(modified_pptx_path, "rb") as f:
        pptx_bytes = f.read()

    return pptx_bytes

def replace_text_in_docx(docx_path, replacements, image_replacements):
    # Caricare il file DOCX
    doc = docx.Document(docx_path)

    # Sostituire i testi nei commenti
    for para in doc.paragraphs:
        for run in para.runs:
            for placeholder, text in replacements.items():
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, text)

    # Sostituire le immagini tramite testo alternativo
    for shape in doc.inline_shapes:
        if shape.type == docx.enum.shape.WD_INLINE_SHAPE.PICTURE or shape.type == 3:
            alt_text = shape._inline.docPr.get('descr')
            for placeholder, image_path in image_replacements.items():
                if alt_text and placeholder in alt_text:
                    # Recupera il "blip" (che contiene il riferimento all'immagine nel pacchetto)
                    blip = shape._inline.graphic.graphicData.pic.blipFill.blip

                    # Sostituisce l'immagine nel pacchetto ZIP del documento
                    with open(image_path, "rb") as new_image_file:
                        new_image_data = new_image_file.read()

                    image_part = doc.part.related_parts[blip.embed]
                    image_part._blob = new_image_data
                    # paragraph = shape._inline.getparent().getparent()

                    # # recupero le dimensioni dell'immagine
                    # width = shape.width
                    # height = shape.height

                    # p = paragraph.getparent()
                    # p.remove(paragraph)

                    # new_run = doc.add_paragraph().add_run()
                    # new_run.add_picture(image_path, width=width, height=height)
                    

    # Salvare il file DOCX modificato
    storage_path = os.path.join("storage", "modificati")
    os.makedirs(storage_path, exist_ok=True)
    modified_docx_path = os.path.join("storage", "modificati", "modified_docx.docx")
    doc.save(modified_docx_path)
    print(f"File DOCX modificato e salvato come '{modified_docx_path}'")

    # Restituire i byte del file PPTX modificato
    with open(modified_docx_path, "rb") as f:
        docx_bytes = f.read()

    return docx_bytes


def duplicate_and_replace_slide(pptx_path, replacements_dict):
    """
    Duplica una slide e applica le sostituzioni di testo e immagine per ogni elemento in replacements_dict.
    
    :param ppt: Presentazione PowerPoint aperta con python-pptx
    :param slide_index: Indice della slide da duplicare
    :param replacements_dict: Dizionario con le sostituzioni di testo e immagine per ogni placeholder
    """
    
    # Carica la presentazione esistente
    ppt = Presentation(pptx_path)

    # Trova le slide con i placeholder
    slides_to_duplicate = []
    for idx, slide in enumerate(ppt.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text.strip()
                for placeholder, data in replacements_dict.items():
                    if text == placeholder:
                        slides_to_duplicate.append((idx, placeholder))
                        break

    # Duplica e modifica le slide
    for slide_idx, placeholder in slides_to_duplicate:
        slide_to_copy = ppt.slides[slide_idx]
        elements = replacements_dict[placeholder]    

        for idx, element in enumerate(elements):
            new_slide = ppt.slides.add_slide(ppt.slide_layouts[6])  # Duplica la slide

            # Inserisci la nuova slide nella stessa posizione della slide originale
            slide_id = ppt.slides._sldIdLst[-1]
            ppt.slides._sldIdLst.remove(slide_id)
            ppt.slides._sldIdLst.insert(slide_idx + idx + 1, slide_id)

            # Copia gli elementi della slide originale nella nuova slide
            for shape in slide_to_copy.shapes:
                if shape.has_text_frame:
                    new_shape = new_slide.shapes.add_textbox(shape.left, shape.top, shape.width, shape.height)
                    new_shape.text = shape.text
                    for i, p in enumerate(shape.text_frame.paragraphs):
                        new_shape.text_frame.paragraphs[i].font.name = p.font.name
                        new_shape.text_frame.paragraphs[i].font.size = p.font.size
                        new_shape.text_frame.paragraphs[i].font.bold = p.font.bold
                        new_shape.text_frame.paragraphs[i].font.italic = p.font.italic
                        new_shape.text_frame.paragraphs[i].font.underline = p.font.underline
                        new_shape.text_frame.paragraphs[i].alignment = p.alignment
                        new_shape.text_frame.paragraphs[i].space_before = p.space_before
                        new_shape.text_frame.paragraphs[i].space_after = p.space_after
                        new_shape.rotation = shape.rotation
                        # new_shape.fill.solid()
                        if p.font.color._color.color_type is not None:
                            new_shape.text_frame.paragraphs[i].font.color.rgb = p.font.color.rgb
                elif shape.shape_type == 13:  # Immagine
                    image_stream = io.BytesIO(shape.image.blob)
                    new_image = new_slide.shapes.add_picture(image_stream, shape.left, shape.top, shape.width, shape.height)
                     # Copia il testo alternativo
                    image_element = shape._element
                    if image_element is not None:
                        cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                        if cNvPr is not None:
                            alt_text = cNvPr.get('descr')
                            new_image._element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}).set('descr', alt_text)
                elif shape.shape_type == 6:  # Gruppo di forme
                    for sub_shape in shape.shapes:
                        if sub_shape.has_text_frame:
                            new_sub_shape = new_slide.shapes.add_textbox(sub_shape.left, sub_shape.top, sub_shape.width, sub_shape.height)
                            new_sub_shape.text = sub_shape.text
                            for i, p in enumerate(sub_shape.text_frame.paragraphs):
                                new_sub_shape.text_frame.paragraphs[i].font.name = p.font.name
                                new_sub_shape.text_frame.paragraphs[i].font.size = p.font.size
                                new_sub_shape.text_frame.paragraphs[i].font.bold = p.font.bold
                                new_sub_shape.text_frame.paragraphs[i].font.italic = p.font.italic
                                new_sub_shape.text_frame.paragraphs[i].font.underline = p.font.underline
                                new_sub_shape.text_frame.paragraphs[i].alignment = p.alignment
                                new_sub_shape.text_frame.paragraphs[i].space_before = p.space_before
                                new_sub_shape.text_frame.paragraphs[i].space_after = p.space_after
                                new_sub_shape.rotation = sub_shape.rotation
                                # new_sub_shape.fill.solid()
                                # if sub_shape.fill.fore_color.type is not None:
                                #     new_sub_shape.fill.fore_color.rgb = sub_shape.fill.fore_color.rgb
                                # if sub_shape.line.color.type is not None:
                                #     new_sub_shape.line.color.rgb = sub_shape.line.color.rgb
                                # new_sub_shape.line.width = sub_shape.line.width
                                if p.font.color._color.color_type is not None:
                                    new_sub_shape.text_frame.paragraphs[i].font.color.rgb = p.font.color.rgb
                        elif sub_shape.shape_type == 13:  # Immagine
                            image_stream = io.BytesIO(sub_shape.image.blob)
                            new_image = new_slide.shapes.add_picture(image_stream, sub_shape.left, sub_shape.top, sub_shape.width, sub_shape.height)
                            # Copia il testo alternativo
                            image_element = sub_shape._element
                            if image_element is not None:
                                cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                                if cNvPr is not None:
                                    alt_text = cNvPr.get('descr')
                                    if alt_text is not None:
                                        new_image._element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}).set('descr', alt_text)
                                    else:
                                        new_image._element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                        else:
                            # Copia altre forme come rettangoli, cerchi, ecc.
                            new_sub_shape = new_slide.shapes.add_shape(sub_shape.auto_shape_type, sub_shape.left, sub_shape.top, sub_shape.width, sub_shape.height)
                            # new_sub_shape.fill.solid()
                            # if sub_shape.fill.fore_color.type is not None:
                            #     new_sub_shape.fill.fore_color.rgb = sub_shape.fill.fore_color.rgb
                            # if sub_shape.line.color.type is not None:
                            #     new_sub_shape.line.color.rgb = sub_shape.line.color.rgb
                            # new_sub_shape.line.width = sub_shape.line.width
                else:
                    # Copia altre forme come rettangoli, cerchi, ecc.
                    new_shape = new_slide.shapes.add_shape(shape.auto_shape_type, shape.left, shape.top, shape.width, shape.height)
                    new_shape.fill.fore_color.rgb = shape.fill.fore_color.rgb
                    new_shape.line.color.rgb = shape.line.color.rgb
                    new_shape.line.width = shape.line.width

            # Sostituzione testo e immagini
            for shape in new_slide.shapes:
                if shape.has_text_frame:
                    text = shape.text.strip()
                    for placeholder, text_change in element["testuali"].items():
                        if text == placeholder:
                            shape.text = text_change 

                elif shape.shape_type == 13:  # 🔹 Sostituzione immagini
                    image_element = shape._element
                    alt_text = None
                    if image_element is not None:
                        cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                        if cNvPr is not None:
                            alt_text = cNvPr.get('descr')

                    for placeholder, image_path in element["immagini"].items():
                        current_image_item = {placeholder: image_path}  # Memorizza l'elemento corrente
                        img_saved = save_image(current_image_item, "storage/immagini/indicatori")
                        if placeholder in shape.image.filename:
                            left, top, width, height = shape.left, shape.top, shape.width, shape.height
                            new_slide.shapes.add_picture(img_saved[placeholder], left, top, width, height)
                        elif alt_text is not None and placeholder in alt_text:
                            left, top, width, height = shape.left, shape.top, shape.width, shape.height
                            new_slide.shapes.add_picture(img_saved[placeholder], left, top, width, height)
                            sp = shape
                            new_slide.shapes._spTree.remove(sp._element)


    return ppt

def save_image(image, image_path):
    """
    in image ho una mappa stringa stringa
    nei valori ho un url di un immagine
    devo fare la chiamata all'url che mi restituisce i byte
    e salvarli in image_path
    """
    saved_images = {
        # "{{immagine_prova1}}": "storage/immagini/image1.png"
    }

    for key, url in image.items():
        response = requests.get(url)
        if response.status_code == 200:
            image = response.content
        else:
            print(f"Errore durante il download dell'immagine da '{url}'")
            continue
        
        if key.startswith("{{"):
            ph = key
        else:
            ph = "{{immagine_"+ key + "}}"
        if key.startswith("C5") or key.startswith("C6") or key.startswith("C7") or key.startswith("{{"):
            key = key + ".png"
        else:
            key = key + ".svg"


        path_save = os.path.join(image_path, key)

        with open(path_save, "wb") as f:
            f.write(image)

        saved_images[ph] = path_save

    return saved_images

def elimina_cartella(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def process_file(file_path, replacements, image_replacements, replacements_for_each):
    # Verifica il tipo di file
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pptx":
        ppt = duplicate_and_replace_slide(file_path, replacements_for_each)
        file_byte = replace_text_in_pptx(ppt, replacements, image_replacements)
        return file_byte
        # replace_text_in_pptx(file_path, replacements, image_replacements)
    elif ext == ".docx":
        file_byte = replace_text_in_docx(file_path, replacements, image_replacements)
        return file_byte
    else:
        print("Tipo di file non supportato. Supportiamo solo .pptx e .docx.")

# # Esempio di utilizzo:
# replacements = {
#     "{{NOME_AZIENDA}}": "Mario Rossi",
#     "{{RUOLO}}": "Chef",
#     "{{azienda_prova}}": "MIND1234567890",
#     "{{TESTO_PROVA}}": "Testo di prova del titolo",
# 	"{{testo_prova_1}}": "Testo di prova del titolo",
# 	"{{testo_prova_2}}": "Testo di prova 2",
#     "Altro testo da cambiare": "Nuovo testo",
#     "XXX": "CIAO"
# }

# image_replacements = {
#      "{{immagine_prova1}}": "storage/immagini/image1.png",  # Inserisci il percorso dell'immagine da sostituire
# }

# # Percorso del file da modificare
# file_path = "storage/powerpoint1.pptx"  # O "path/to/your/file.docx"

# # Processare il file
# process_file(file_path, replacements, image_replacements)
