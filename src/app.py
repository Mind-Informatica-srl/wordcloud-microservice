from flask import Flask, request, send_file, jsonify
from barre_graph import generate_barre_in_pila
from barre_graph import generate_barre_in_pila_serie_s
from dispersione import generate_dispersione
from overaly_images import overlayimages
from pie3d_graph import generate_pie3d
from risk_bar import create_risk_bar_chart
from risk_line import create_risk_line_chart
from wordcloud_graph import generate_wordcloud
from barre_orizzontali import generate_barre_orizzontali
from distribuzione import create_survey_chart
from mod_office import process_file
import io
import os
from PIL import Image

app = Flask(__name__)

mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "svg": "image/svg+xml",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate_wordcloud', methods=['POST'])
def create_wordcloud():
    data = request.json
    print(data)  # Stampa data in console
    word_colors = data.get('wordColors', {})
    word_frequencies = data.get('wordFrequencies', {})
    default_color = data.get('default_color', '#000000')
    format = data.get('format', 'png')

    try:
        image_bytes = generate_wordcloud(word_colors, word_frequencies, default_color, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = generate_barre_in_pila(colors, labels, sizes, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = generate_barre_in_pila_serie_s(colors, sizes, fasce, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = generate_barre_orizzontali(colors, labels, sizes, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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


    try:
        image_bytes = create_survey_chart(survey_data, cn, c, format, cl)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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


    try:
        image_bytes = generate_pie3d(colors, labels, sizes, explode, title, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = generate_dispersione(x, y, labels, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = create_risk_bar_chart(categories, values, groups, risk_zones, risk_colors, legend_labels, bar_colors, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
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

    try:
        image_bytes = create_risk_line_chart(categories, values, risk_zones, risk_colors, legend_labels, format)
        return send_file(io.BytesIO(image_bytes), mimetype=mime_types[format])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/modify-office', methods=['POST'])
def modifica_office():
    replacements = {
    "{NOME}": "Mario Rossi",
    "{RUOLO}": "Chef",
    "{{azienda_prova}}": "MIND1234567890",
	"{{testo_prova_1}}": "Testo di prova del titolo",
	"{{testo_prova_2}}": "Testo di prova 2",
    }

    image_replacements = {
    # "image.png": "storage/image1.png",  # Inserisci il percorso dell'immagine da sostituire
    "{{immagine_prova1}}": "storage/image1.png"  # Inserisci il percorso dell'immagine da sostituire
    }

    # Percorso del file da modificare
    file_path = "storage/immagine.docx"  # O "path/to/your/file.docx"

    # Processare il file
    process_file(file_path, replacements, image_replacements)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)