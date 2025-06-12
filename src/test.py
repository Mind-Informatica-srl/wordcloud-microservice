import json
import os

from flask import jsonify

from mod_office import process_file


def test_stampa():
    name = 'PARTE 3.docx'  # Nome del file da modificare
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '..', 'storage', 'valori_request.json')  # Percorso assoluto
    print (f"JSON Path: {json_path}", flush=True)

    file_path = os.path.join(base_dir, '..', 'storage', name)
    path_save = os.path.join(base_dir, '..', 'storage', 'immagini')
    os.makedirs(path_save, exist_ok=True)
    indicatori_path = os.path.join(path_save, 'indicatori')
    os.makedirs(indicatori_path, exist_ok=True)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        replacements = data.get('testuali', [])
        if not replacements:
            print("Nessun testo da sostituire trovato nel file JSON.", flush=True)
            return jsonify({'message': 'Nessun testo da sostituire trovato.'}), 200
        else:
            print(f"Replacements: {replacements}", flush=True)
        image_replacements = data.get('immagini', [])
        if not image_replacements:
            print("Nessuna immagine da sostituire trovata nel file JSON.", flush=True)
            return jsonify({'message': 'Nessuna immagine da sostituire trovata.'}), 200
        else:
            print(f"Image replacements: {image_replacements}", flush=True)
        replacements_for_each = data.get('ciclici', [])
        if not replacements_for_each:
            print("Nessun testo ciclico da sostituire trovato nel file JSON.", flush=True)
            return jsonify({'message': 'Nessun testo ciclico da sostituire trovato.'}), 200
        else:
            print(f"Replacements for each: {replacements_for_each}", flush=True)
    except Exception as e:
        print(f"Errore nel caricamento del JSON: {e}", flush=True)
        return
    

    try:
        print(f"File Path: {file_path}", flush=True)
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except Exception as e:
        print(f"Errore nella lettura del file: {e}", flush=True)
        return

    try:
        print("Inizio il processo di sostituzione...", flush=True)
        # Processare il file
        fileByte = process_file(file_path, replacements, image_replacements, replacements_for_each, base_dir)
        # elimina_cartella(UPLOAD_FOLDER)
        if not fileByte:
            print("Nessun file generato.", flush=True)
            return jsonify({'message': 'Nessun file generato.'}), 200
        print("File processato con successo.", flush=True)
        return fileByte
    except Exception as e:
        print(str(e), flush=True)
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    test_stampa()
    print("Test completato.", flush=True)