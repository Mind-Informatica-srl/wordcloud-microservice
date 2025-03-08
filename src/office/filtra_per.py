def filtra_per(ppt, replacements):
    """
        controllo tutte le slide, se la slide possiede la stringa {{if:val:*}}
        se non esiste vado avanti
        se esiste controllo se la stringa è uguale a quella passata
        se è uguale la tengo
        se non è uguale la elimino
    """
    slides_to_remove = []

    for count, slide in enumerate(ppt.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
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
                                if ph not in replacements.keys() or replacements[ph] is None or replacements[ph] == '':
                                    slides_to_remove.append(count)
                                    break
                                elif replacements[ph] is not None and replacements[ph] != '':
                                    para.text = para.text.replace("{{if:" + condition + "}}", "")
                            elif v == "":
                                if ph in replacements.keys() and replacements[ph] == '':
                                    slides_to_remove.append(count)
                                    break
                                elif ph not in replacements.keys():
                                    para.text = para.text.replace("{{if:" + condition + "}}", "")
                            else:
                                if replacements[ph] != v:
                                    slides_to_remove.append(count)
                                    break
                                elif replacements[ph] == v:
                                    para.text = para.text.replace("{{if:" + condition + "}}", "")

    # Elimina le slide raccolte
    for idx in sorted(slides_to_remove, reverse=True):
        rId = ppt.slides._sldIdLst[idx].rId
        if ppt.part.rels.get(rId):
            ppt.part.drop_rel(rId)
        del ppt.slides._sldIdLst[idx]

    # # eliminare tutte le relazioni che non sono più utilizzate
    # rels_to_remove = []
    # for rel in ppt.part.rels:
    #     rel_part = ppt.part.rels[rel].target_part
    #     rel_name = rel_part._partname
    #     if rel_name not in [slide.part._partname for slide in ppt.slides]:
    #         rels_to_remove.append(rel)
    
    # # ordino le relazioni in modo che siano in ordine inverso
    # rels_to_remove.sort(reverse=True)
    # for rel in rels_to_remove:
    #     ppt.part.drop_rel(rel)