import copy
from pptx import Presentation
import docx
import os
import requests
import shutil
import io
import re
from python_pptx_text_replacer import TextReplacer

from constants import UPLOAD_FOLDER
from office.duplicate_and_replace_slide import duplicate_and_replace_slide
from office.filtra_per_tipo_woseq import filtra_per_tipo_woseq
from office.save_image import save_image


def replace_text_in_pptx(ppt, replacements, image_replacements):
    # Sostituire i testi nei segnaposto
    for slide in ppt.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        words = run.text.split()
                        new_text = []
                        for word in words:
                            for placeholder, text in replacements.items():
                                if placeholder in word:
                                    word = word.replace(placeholder, text)
                            new_text.append(word)
                        run.text = ' '.join(new_text)
            elif shape.shape_type == 6:  # Gruppo di forme
                for sub_shape in shape.shapes:
                    if sub_shape.has_text_frame:
                        for para in sub_shape.text_frame.paragraphs:
                            for run in para.runs:
                                words = run.text.split()
                                new_text = []
                                for word in words:
                                    for placeholder, text in replacements.items():
                                        if placeholder in word:
                                            word = word.replace(placeholder, text)
                                    new_text.append(word)
                                run.text = ' '.join(new_text)


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
                        imaga_saved = save_image(placeholder, image_path, "storage/immagini")
                        slide.shapes.add_picture(imaga_saved[placeholder], left, top, width, height)
                    elif alt_text is not None and placeholder in alt_text:
                        # Posizione e dimensioni dell'immagine
                        left, top, width, height = shape.left, shape.top, shape.width, shape.height
                        # Aggiungere la nuova immagine
                        imaga_saved = save_image(placeholder, image_path, "storage/immagini")
                        slide.shapes.add_picture(imaga_saved[placeholder], left, top, width, height)
                        # Rimuove l'immagine originale
                        sp = shape
                        slide.shapes._spTree.remove(sp._element)

    return ppt

def salva_byte_pptx(ppt):
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

def elimina_cartella(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def process_file(file_path, replacements, image_replacements, replacements_for_each):
    changed_presentation = os.path.join(UPLOAD_FOLDER, "changed.pptx")
    ppt = Presentation(file_path)
    filtra_per_tipo_woseq(ppt, replacements)
    for_indexes = duplicate_and_replace_slide(ppt, replacements_for_each)
    with open(changed_presentation, 'wb') as f:
        ppt.save(f)
    replacements_t = [(placeholder, text) for placeholder, text in replacements.items()]
    replacer = TextReplacer(changed_presentation, slides='', tables=True, charts=True, textframes=True)
    replacer.replace_text(replacements_t)
    replacer.write_presentation_to_file(changed_presentation)
    for for_type, sequences in for_indexes.items():
        reps = replacements_for_each.get(for_type)
        for sequence in sequences:
            for ind, sliden in enumerate(sequence):
                slidenstr = str(sliden+1)
                replacer = TextReplacer(changed_presentation, slides=slidenstr, tables=True, charts=True, textframes=True)
                rep = reps[ind]['testuali']
                rep_t = [(placeholder, text) for placeholder, text in rep.items()]
                replacer.replace_text(rep_t)
                replacer.write_presentation_to_file(changed_presentation)
            
    with open(changed_presentation, 'rb') as f:
        file = f.read()
    return file
    
    # Verifica il tipo di file
    # ext = os.path.splitext(file_path)[1].lower()

    # for key, value in replacements.items():
    #     if key.startswith("{{if_tipo_woseq:") and key.endswith("}}"):
    #         if_tipo_woseq = key

    # if ext == ".pptx":
    #     ppt = Presentation(file_path)
    #     ppt = flitra_per_tipo_woseq(ppt, if_tipo_woseq)
    #     ppt = duplicate_and_replace_slide(ppt, replacements_for_each)
    #     ppt = replace_text_in_pptx(ppt, replacements, image_replacements)
    #     file_byte = salva_byte_pptx(ppt)
    #     return file_byte
    #     # replace_text_in_pptx(file_path, replacements, image_replacements)
    # elif ext == ".docx":
    #     file_byte = replace_text_in_docx(file_path, replacements, image_replacements)
    #     return file_byte
    # else:
    #     print("Tipo di file non supportato. Supportiamo solo .pptx e .docx.")

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
