import os

import ssl
import urllib.request

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
    # if key not in [
    #     "{{azioni_miglioramento_proposte}}",
    #     "{{semaforo_gruppo_omogeneo}}",
    #     "{{eventi_gruppo_omogeneo}}",
    #     "{{indicatori_eventi}}",
    #     "{{spiegazione_evento_go}}"
    # ]:
    #     url = os.getenv("BASE_URL") + url + f"&width={width}&height={height}"
    # else:
    #     url = os.getenv("BASE_URL") + url + f"?width={width}&height={height}"
    # print(f"Sto per chiamare '{url}'")
    params = {"width": width, "height": height}
    if key not in [
        "{{azioni_miglioramento_proposte}}",
        "{{semaforo_gruppo_omogeneo}}",
        "{{eventi_gruppo_omogeneo}}",
        "{{indicatori_eventi}}",
        "{{spiegazione_evento_go}}"
    ]:
        # url potrebbe già avere parametri, aggiungi anche quelli nuovi
        if "?" in url:
            url_base, query = url.split("?", 1)
            query_dict = dict(urllib.parse.parse_qsl(query))
            query_dict.update(params)
            url = url_base + "?" + urllib.parse.urlencode(query_dict)
        else:
            url = url + "?" + urllib.parse.urlencode(params)
    else:
        url = url + "?" + urllib.parse.urlencode(params)
    url = os.getenv("BASE_URL") + url
    print(f"Sto per chiamare '{url}'")
    

    try:
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=ssl_context) as response:
            if response.status == 200:
                image_bytes = response.read()
            else:
                print(f"Errore durante il download dell'immagine da '{url}'")
                return saved_images
    except Exception as e:
        return {"error": str(e)}
        # print(f"Eccezione durante il download dell'immagine da '{url}': {e}")
        # return saved_images
    
    
    # Salvare l'immagine
    k = key
    key_clean = key.replace("{{", "").replace("}}", "")
    ph = key_clean + ".png"
    path_save = os.path.join(image_path, ph)
    with open(path_save, "wb") as f:
        f.write(image_bytes)
    saved_images[k] = path_save

    return saved_images