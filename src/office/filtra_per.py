def filtra_per(ppt, replacements):
    """
        controllo tutte le slide, se la slide possiede la stringa {{if_tipo_woseq:
        se non esiste vado avanti
        se esiste controllo se la stringa è uguale a quella passata
        se è uguale la tengo
        se non è uguale la elimino
    """
    # dichiaro un array in cui metto gli indici delle slide da eliminare
    slides_to_remove = []
    # ciclo tutte le slide
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
                            t = para.text.replace("{{", "").replace("}}", "")
                            parts = t.split(":")
                            if len(parts) == 3:
                                ph = "{{" +  parts[1] + "}}"
                                v = parts[2]
                            else:
                                continue

                            if v == "*":
                                if ph not in replacements.keys():
                                    # rId = ppt.slides._sldIdLst[count].rId
                                    # ppt.part.drop_rel(rId)
                                    # del ppt.slides._sldIdLst[count]
                                    slides_to_remove.append(count)
                                    rimossa = True
                                elif replacements[ph] is None or replacements[ph] == '':
                                    # rId = ppt.slides._sldIdLst[count].rId
                                    # ppt.part.drop_rel(rId)
                                    # del ppt.slides._sldIdLst[count]
                                    slides_to_remove.append(count)
                                    rimossa = True
                                elif replacements[ph] is not None and replacements[ph] != '':
                                    para.text = ""
                            else:
                                if replacements[ph] != v:
                                    # rId = ppt.slides._sldIdLst[count].rId
                                    # ppt.part.drop_rel(rId)
                                    # del ppt.slides._sldIdLst[count]
                                    slides_to_remove.append(count)
                                    rimossa = True
                                elif replacements[ph]== v:
                                    para.text = ""
            count += 1
        if not rimossa:
            break
        rimossa = False
    # rimuovo le slide partendo dall'ultima
    for i in range(len(slides_to_remove)-1, -1, -1):
        index = slides_to_remove[i]
        rId = ppt.slides._sldIdLst[index].rId
        ppt.part.drop_rel(rId)
        del ppt.slides._sldIdLst[index]