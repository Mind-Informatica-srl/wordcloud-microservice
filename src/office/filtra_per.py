def filtra_per(ppt, replacements):
    """
        controllo tutte le slide, se la slide possiede la stringa {{if:val:*}}
        se non esiste vado avanti
        se esiste controllo se la stringa è uguale a quella passata
        se è uguale la tengo
        se non è uguale la elimino
    """
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

                        if para.text.startswith("{{if:"):
                            conditions = [cond.split("}}")[0].strip() for cond in para.text.split("{{if:") if "}}" in cond]
                            for condition in conditions:
                                t = condition
                                parts = t.split(":")
                                if len(parts) == 2:
                                    ph = "{{" + parts[0] + "}}"
                                    v = parts[1]
                                else:
                                    continue


                                if v == "*":
                                    if ph not in replacements.keys():
                                        rId = ppt.slides._sldIdLst[count].rId
                                        ppt.part.drop_rel(rId)
                                        del ppt.slides._sldIdLst[count]
                                        rimossa = True
                                    elif replacements[ph] is None or replacements[ph] == '':
                                        rId = ppt.slides._sldIdLst[count].rId
                                        ppt.part.drop_rel(rId)
                                        del ppt.slides._sldIdLst[count]
                                        rimossa = True
                                    elif replacements[ph] is not None and replacements[ph] != '':
                                        para.text = para.text.replace("{{if:" + condition + "}}", "")
                                elif v == "":
                                    if ph in replacements.keys() and replacements[ph] == '':
                                        rId = ppt.slides._sldIdLst[count].rId
                                        ppt.part.drop_rel(rId)
                                        del ppt.slides._sldIdLst[count]
                                        rimossa = True
                                    elif ph not in replacements.keys():
                                        para.text = para.text.replace("{{if:" + condition + "}}", "")
                                else:
                                    if replacements[ph] != v:
                                        rId = ppt.slides._sldIdLst[count].rId
                                        ppt.part.drop_rel(rId)
                                        del ppt.slides._sldIdLst[count]
                                        rimossa = True
                                    elif replacements[ph]== v:
                                        para.text = para.text.replace("{{if:" + condition + "}}", "")
            count += 1
        if not rimossa:
            break
        rimossa = False