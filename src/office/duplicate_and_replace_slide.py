import copy
import io
import re

from office.save_image import save_image

def print_slide_names(ppt):
    # Stampa i nomi delle slide
    for idx, slide in enumerate(ppt.slides):
        slide_name = f"slide{idx + 1}.xml"
        print(f"Slide name: {slide_name}")

    # Stampa i nomi delle relazioni
    for rel in ppt.part.rels:
        rel_part = ppt.part.rels[rel].target_part
        rel_name = rel_part.partname
        print(f"Relationship name: {rel_name}")

def extract_placeholder_info(text):
    """
    Estrae il placeholder  dal testo e restituisce n come intero.
    """
    match = re.search(r"{{([^:]+):(\d+)}}", text)
    if match:
        return "{{"+match.group(1)+":n}}", "{{"+match.group(1)+"}}", int(match.group(2))
    return None


def duplicate_and_replace_slide(ppt, replacements_dict, num_fg, num_go):
    """
    Duplica una slide e applica le sostituzioni di testo e immagine per ogni elemento in replacements_dict.
    
    :param ppt: Presentazione PowerPoint aperta con python-pptx
    :param slide_index: Indice della slide da duplicare
    :param replacements_dict: Dizionario con le sostituzioni di testo e immagine per ogni placeholder
    """

    # Stampa le slide
    print_slide_names(ppt)

    print(ppt.slides._sldIdLst)

    
    # Trova le slide con i placeholder
    slides_to_duplicate = []
    for idx, slide in enumerate(ppt.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text.strip()
                for placeholder, _ in replacements_dict.items():
                    n = extract_placeholder_info(text)
                    if n is not None:
                        if n[0] == placeholder:
                            slides_to_duplicate.append((idx, n[2], n[0]))
                            shape.text = ""
                            break
    
    # dichiaro slides_to_elaborate come mappa di stringa - array di interi
    slides_to_elaborate = {}
    # Duplica e modifica le slide
    for slide_idx, num_duplicates, forplaceholder in slides_to_duplicate:
        if slides_to_elaborate.get(forplaceholder) is None:
            slides_to_elaborate[forplaceholder] = []
        ids = [slide_idx]
        slide_to_copy = ppt.slides[slide_idx]
        elements = replacements_dict[forplaceholder]  

        slide_copy = copy.deepcopy(slide_to_copy)  

        # recupero il numero di focus group e il numero di di gruppi omogenei per capire quante slide dovrò replicare
        num_replace = 0
        if forplaceholder == "{{for_fg:n}}":
            num_replace = -(-int(num_fg) // num_duplicates)  # Arrotonda per eccesso
        elif forplaceholder == "{{for_go:n}}":
            num_replace = -(-int(num_go) // num_duplicates)

        for idx in range(num_replace):
            if idx == 0:
                new_slide = slide_to_copy
            else:
                new_slide = None
                new_slide = ppt.slides.add_slide(ppt.slide_layouts[6])  # Duplica la slide

                # Inserisci la nuova slide nella stessa posizione della slide originale
                slide_id = ppt.slides._sldIdLst[-1]
                ppt.slides._sldIdLst.remove(slide_id)
                newindex = slide_idx + idx
                ppt.slides._sldIdLst.insert(newindex, slide_id)
                ids.append(newindex)

                # Copia gli elementi della slide originale nella nuova slide
                for shape in slide_copy.shapes:
                    if shape.shape_type == 13:  # Immagine
                        image_stream = io.BytesIO(shape.image.blob)
                        new_image = new_slide.shapes.add_picture(image_stream, shape.left, shape.top, shape.width, shape.height)
                        # Copia il testo alternativo
                        image_element = shape._element
                        if image_element is not None:
                            cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                            if cNvPr is not None:
                                alt_text = cNvPr.get('descr')
                                if alt_text is not None:
                                    new_image._element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}).set('descr', alt_text)
                    else:
                        el = shape.element
                        new_shape = copy.deepcopy(el)
                        new_slide.shapes._spTree.insert_element_before(new_shape, 'p:extLst')

            # Sostituzione testo e immagini
            for shape in new_slide.shapes:
                if shape.shape_type == 13:  # Sostituzione immagini
                    image_element = shape._element
                    alt_text = None
                    if image_element is not None:
                        cNvPr = image_element.find('.//p:cNvPr', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
                        if cNvPr is not None:
                            alt_text = cNvPr.get('descr')

                    # controllo se il placeholder è della forma {{testo:n}}
                    if alt_text is not None:
                        t = extract_placeholder_info(alt_text)
                        if t is not None:
                        # n del placeholder (index_slide)
                        # recupero e ricreo il placeholder (placeholder_slide)
                            placeholder_slide = t[1]
                            index_slide = t[2]

                            # recupero l'indice del placeholder
                            index = (index_slide - 1) + (idx * num_duplicates)
                            element = elements[index]

                            for placeholder, image_path in element["immagini"].items():
                                if (placeholder in shape.image.filename) or (alt_text is not None and placeholder in placeholder_slide):
                                    img_saved = save_image(placeholder, image_path, "storage/immagini/indicatori")
                                    left, top, width, height = shape.left, shape.top, shape.width, shape.height
                                    new_slide.shapes.add_picture(img_saved[placeholder], left, top, width, height)
                                    sp = shape
                                    new_slide.shapes._spTree.remove(sp._element)

        idsList = slides_to_elaborate.get(forplaceholder)
        if idsList is None:
            idsList = []
        idsList.append(ids)
        slides_to_elaborate[forplaceholder] = idsList

        print_slide_names(ppt)

    return slides_to_elaborate