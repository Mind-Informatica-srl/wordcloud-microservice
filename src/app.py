from flask import Flask, request, send_file, jsonify, make_response
from barre_graph import generate_barre_in_pila
from barre_graph import generate_barre_in_pila_serie_s
from constants import UPLOAD_FOLDER
from dispersione import generate_dispersione
from overaly_images import overlayimages
from pie3d_graph import generate_pie3d
from risk_bar import create_risk_bar_chart
from risk_line import create_risk_line_chart
from wordcloud_graph import generate_wordcloud
from barre_orizzontali import generate_barre_orizzontali
from distribuzione import create_survey_chart
from mod_office import process_file, elimina_cartella
from generate_list import generate_list, generate_fonti_list
import io
import os
from PIL import Image
import base64
import logging

app = Flask(__name__)

# Configura il logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "svg": "image/svg+xml",
        "SVG": "image/svg+xml",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate_wordcloud', methods=['POST'])
def create_wordcloud():
    data = request.json
    print(data)  # Stampa data in console
    word_colors = data.get('wordColors', {})
    word_frequencies = data.get('wordFrequencies', {})
    default_color = data.get('default_color', '#000000')
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_wordcloud(word_colors, word_frequencies, default_color, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        ## return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_list', methods=['POST'])
def create_list():
    data = request.json
    print(data)
    items = data.get('items', [])
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_list(items, format, width, height)
        return send_file(image_bytes, mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_fonti_list', methods=['POST'])
def create_fonti_list():
    data = request.json
    print(data)
    items = data.get('items', [])
    format = data.get('format', 'png')

    try:
        image_bytes = generate_fonti_list(items, format)
        return send_file(image_bytes, mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/overlay_images', methods=['POST'])
def overlay_images():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Both image1 and image2 are required'}), 400

    image1 = Image.open(request.files['image1'])
    image2 = Image.open(request.files['image2'])

    # Ensure both images have the same size
    image2 = image2.resize(image1.size)

    # Overlay images
    img_byte_arr = overlayimages(image1, image2)

    return send_file(img_byte_arr, mimetype='image/svg+xml')

@app.route('/generate_barre_in_pila', methods=['POST'])
def create_barre_in_pila():
    data = request.json
    print(data)
    colors = data.get('colors', [])
    labels = data.get('labels', [])
    sizes = data.get('sizes', [])
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_barre_in_pila(colors, labels, sizes, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_barre_in_pila_serie_s', methods=['POST'])
def create_barre_in_pila_serie_s():
    data = request.json
    print(data)
    colors = data.get('colors', [])
    sizes = data.get('sizes', [])
    format = data.get('format', 'png')
    fasce = data.get('fasce_confidenza', [])
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_barre_in_pila_serie_s(colors, sizes, fasce, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_barre_orizzontali', methods=['POST'])
def create_barre_orizzontali():
    data = request.json
    print(data)
    colors = data.get('colors', [])
    labels = data.get('labels', [])
    sizes = data.get('sizes', [])
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_barre_orizzontali(colors, labels, sizes, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
@app.route('/distribuzione', methods=['POST'])
def create_distribuzione():
    data = request.json
    print(data)
    survey_data = data.get('data', [])
    cn = data.get('category_names', [])
    c = data.get('colors', [])
    format = data.get('format', 'png')
    cl = data.get('color_labels', [])
    width = data.get('width', 610)
    height = data.get('height', 180)


    try:
        image_bytes = create_survey_chart(survey_data, cn, c, format, cl, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_pie3d', methods=['POST'])
def create_pie3d():
    data = request.json
    print(data)
    colors = data.get('colors', [])
    labels = data.get('labels', [])
    sizes = data.get('sizes', [])
    explode = data.get('explode', [])
    title = data.get('title', '3D Pie Chart')
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)


    try:
        image_bytes = generate_pie3d(colors, labels, sizes, explode, title, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/dispersione', methods=['POST'])
def create_dispersione():
    data = request.json
    print(data)
    x = data.get('x', [])
    y = data.get('y', [])
    labels = data.get('labels', [])
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = generate_dispersione(x, y, labels, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/risk_bar', methods=['POST'])
def create_risk_bar():
    data = request.json
    print(data)
    categories = data.get('categories', [])
    values = data.get('values', [])
    groups = data.get('groups', [])
    risk_zones = data.get('risk_zones', [])
    risk_colors = data.get('risk_colors', [])
    legend_labels = data.get('legend_labels', [])
    bar_colors = data.get('bar_colors', []) 
    format = data.get('format', 'png')
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = create_risk_bar_chart(categories, values, groups, risk_zones, risk_colors, legend_labels, bar_colors, format, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/risk_line', methods=['POST'])
def create_risk_line():
    data = request.json
    print(data)
    categories = data.get('categories', [])
    values = data.get('values', [])
    risk_zones = data.get('risk_zones', [])
    risk_colors = data.get('risk_colors', [])
    legend_labels = data.get('legend_labels', [])
    format = data.get('format', 'png')
    is_white = data.get('is_white', False)
    width = data.get('width', 610)
    height = data.get('height', 180)

    try:
        image_bytes = create_risk_line_chart(categories, values, risk_zones, risk_colors, legend_labels, format, is_white, width, height)
        buffer = io.BytesIO(image_bytes)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[format])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Content-Disposition', 'inline; filename=wordcloud.' + format)
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/modify-office', methods=['POST'])
def modifica_office():
    data = request.json
    name = data.get('name', 'pp.pptx')
    file = data.get('file', '')
    # decodifica il file in base64
    file = base64.b64decode(file)

    replacements = data.get('testuali', [])
    # trasformo replacements in una lista di tuple con chiave e valore
    image_replacements = data.get('immagini', [])
    replacements_for_each = data.get('ciclici', [])

    file_path = os.path.join(UPLOAD_FOLDER, name)
    path_save = os.path.join(UPLOAD_FOLDER, 'immagini')
    os.makedirs(path_save, exist_ok=True)
    indicatori_path = os.path.join(path_save, 'indicatori')
    os.makedirs(indicatori_path, exist_ok=True)

    # image_saved = save_image(image_replacements, path_save)
    # file_byte = bytes(file, 'utf-8')
    ext = os.path.splitext(name)[1][1:].lower()
    

    try:
        with open(file_path, 'wb') as f:
            f.write(file)
    except Exception as e:
        app.logger.error(f"Errore durante il salvataggio del file: {e}")
        print(f"Errore durante il salvataggio del file: {e}", flush=True)
        return jsonify({'error': str(e)}), 500

    try:
        # Processare il file
        fileByte = process_file(file_path, replacements, image_replacements, replacements_for_each)
        elimina_cartella(UPLOAD_FOLDER)
        buffer = io.BytesIO(fileByte)
        response = make_response(buffer.read())
        response.headers.set('Content-Type', mime_types[ext])
        response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        response.headers.set('Pragma', 'no-cache')
        response.headers.set('Expires', '0')
        return response
        # return send_file(io.BytesIO(fileByte), mimetype=mime_types[ext])
    except Exception as e:
        app.logger.error(f"Errore durante la modifica del file: {e}")
        print(str(e), flush=True)
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)