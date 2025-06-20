import os

import requests


def save_image(key, url, image_path, width, height):
    """
    in image ho una mappa stringa stringa
    nei valori ho un url di un immagine
    devo fare la chiamata all'url che mi restituisce i byte
    e salvarli in image_path
    """
    saved_images = {
        # "{{immagine_prova1}}": "storage/immagini/image1.png"
    }
    if key != "{{azioni_miglioramento_proposte}}" and key != "{{semaforo_gruppo_omogeneo}}" and key != "{{eventi_gruppo_omogeneo}}" and key != "{{indicatori_eventi}}" and key != "{{spiegazione_evento_go}}":
        url = os.getenv("BASE_URL") + url + f"&width={width}&height={height}"
    else:
        url = os.getenv("BASE_URL") + url + f"?width={width}&height={height}"
    print(f"Sto per chiamare '{url}'")
    

    response = requests.get(url)
    if response.status_code == 200:
        image = response.content
    else:
        print(f"Errore durante il download dell'immagine da '{url}'")
    
    # Salvare l'immagine
    k = key
    key = key.replace("{{", "").replace("}}", "")
    ph = key + ".png"
    path_save = os.path.join(image_path, ph)
    with open(path_save, "wb") as f:
        f.write(image)
    saved_images[k] = path_save

    return saved_images