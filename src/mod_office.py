from pptx import Presentation
import docx
from docx.shared import Inches
import os

def replace_text_in_pptx(pptx_path, replacements, image_replacements):
    # Caricare il file PPTX
    ppt = Presentation(pptx_path)

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
    modified_pptx_path = "modified_pptx.pptx"
    ppt.save(modified_pptx_path)
    print(f"File PPTX modificato e salvato come '{modified_pptx_path}'")

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
    modified_docx_path = "modified_docx.docx"
    doc.save(modified_docx_path)
    print(f"File DOCX modificato e salvato come '{modified_docx_path}'")


def process_file(file_path, replacements, image_replacements):
    # Verifica il tipo di file
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pptx":
        replace_text_in_pptx(file_path, replacements, image_replacements)
    elif ext == ".docx":
        replace_text_in_docx(file_path, replacements, image_replacements)
    else:
        print("Tipo di file non supportato. Supportiamo solo .pptx e .docx.")

# Esempio di utilizzo:
replacements = {
    "{{NOME_AZIENDA}}": "Mario Rossi",
    "{{RUOLO}}": "Chef",
    "{{azienda_prova}}": "MIND1234567890",
    "{{TESTO_PROVA}}": "Testo di prova del titolo",
	"{{testo_prova_1}}": "Testo di prova del titolo",
	"{{testo_prova_2}}": "Testo di prova 2",
    "Altro testo da cambiare": "Nuovo testo",
    "XXX": "CIAO"
}

image_replacements = {
     "{{immagine_prova1}}": "storage/image1.png",  # Inserisci il percorso dell'immagine da sostituire
}

# Percorso del file da modificare
file_path = "storage/immagine.docx"  # O "path/to/your/file.docx"

# Processare il file
process_file(file_path, replacements, image_replacements)
