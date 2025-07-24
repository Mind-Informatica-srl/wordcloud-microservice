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
    if key not in [
        "{{azioni_miglioramento_proposte}}",
        "{{semaforo_gruppo_omogeneo}}",
        "{{eventi_gruppo_omogeneo}}",
        "{{indicatori_eventi}}",
        "{{spiegazione_evento_go}}"
    ]:
        url = os.getenv("BASE_URL") + url + f"&width={width}&height={height}"
    else:
        url = os.getenv("BASE_URL") + url + f"?width={width}&height={height}"
    print(f"Sto per chiamare '{url}'")
    

    response = requests.get(url)
    if response.status_code == 200:
        image_bytes = response.content
            # Salvare l'immagine
        k = key
        key_clean = key.replace("{{", "").replace("}}", "")
        ph = key_clean + ".png"
        path_save = os.path.join(image_path, ph)
        with open(path_save, "wb") as f:
            f.write(image_bytes)
        saved_images[k] = path_save
    else:
        print(f"Errore durante il download dell'immagine da '{url}'")

    return saved_images