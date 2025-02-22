def filtra_per_tipo_woseq(ppt, replacements):
    """
        controllo tutte le slide, se la slide possiede la stringa {{if_tipo_woseq:
        se non esiste vado avanti
        se esiste controllo se la stringa è uguale a quella passata
        se è uguale la tengo
        se non è uguale la elimino
    """
    for key, _ in replacements.items():
        if key.startswith("{{if_tipo_woseq:") and key.endswith("}}"):
            tipo_woseq = key
            break
    if tipo_woseq is None:
        return
    rimossa = False
    while True:
        count = 0
        for slide in ppt.slides:
            if rimossa:
                break
            for shape in slide.shapes:
                if rimossa:
                    break
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        if rimossa:
                            break
                        if para.text.startswith("{{if_tipo_woseq:"):
                            if para.text != tipo_woseq:
                                rId = ppt.slides._sldIdLst[count].rId
                                ppt.part.drop_rel(rId)
                                del ppt.slides._sldIdLst[count]
                                rimossa = True
                            else:
                                para.text = ''
            count += 1
        if not rimossa:
            break
        rimossa = False