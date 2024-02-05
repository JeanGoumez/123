from flask import Flask,jsonify,request,url_for,send_from_directory
import requests
import os
import uuid
import cv2 
from utils import recortar_rostros

#Umbral del imagen en px para ser redimensionada
LIMITE_DIMENSION = 1500
#Reducir las dimensiones a escala 600 px
REDIRECCIONAR = 600

#Margen adicional para el recorte
MARGEN_ANCHURA = 0.20
MARGEN_ALTURA = 0.33
MARGEN_ALTURA_CABEZA = 0.15

app = Flask(__name__)

UPLOAD_FOLDER = 'imagen_descargada' 
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def hello():
    return "Aplicacion de procesamiento de imagen"


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    data = request.json
    
    if 'url_imagen' in data:
        url_imagen = data['url_imagen']
        
        # Descargar la imagen desde la URL
        response = requests.get(url_imagen)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            img_id = str(uuid.uuid4())
            img_name = f'imagen_{img_id}.jpg'
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            
            with open(img_path, 'wb') as f:
                f.write(response.content)

            image = cv2.imread(img_path)
            height, width, _ = image.shape
            
            if height > LIMITE_DIMENSION or width > LIMITE_DIMENSION:
                # Redimensionamos la imagen si supera las dimensiones maxima
                if height > width:
                    new_height = REDIRECCIONAR
                    new_width = int(width * (REDIRECCIONAR / height))
                else:
                    new_width = REDIRECCIONAR
                    new_height = int(height * (REDIRECCIONAR / width))
                    
                # image = cv2.resize(image, (new_width, new_height))
            image_procesada = recortar_rostros(img_path)

            if image_procesada is not None:
                # Guardar la imagen procesada en la carpeta de salida
                img_name_procesada = f'procesada_{img_name}'
                img_path_procesada = os.path.join(app.config['UPLOAD_FOLDER'], img_name_procesada)
                cv2.imwrite(img_path_procesada, image_procesada)
                
                # Obtener la URL de la imagen procesada
                url_imagen_procesada = url_for('uploaded_file', filename=img_name_procesada) 
                
                # Número de rostros identificados, si lo deseas
                # num_rostros = len(rostros)
                
                response_json = {
                    "url_imagen_procesada": url_imagen_procesada,
                    # "cantidad_rostros_identificados": num_rostros,
                }
                return jsonify(response_json)
            else:
                return jsonify({"mensaje": "No se encontraron rostros en la imagen o hubo un error en el procesamiento"})
         
        else:
            return "No se pudo descargar la imagen", 400
    else:
        return "No se proporcionó la URL de la imagen en el JSON", 400

@app.route('/procesar_carpeta', methods=['POST'])
def procesar_carpeta():
    input_folder = 'input'
    output_folder = 'output'
     
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Obtener las imagenes de la carpeta input
    lista_imagenes = os.listdir(input_folder)
    
    if not lista_imagenes:
        return jsonify({"mensaje": "La carpeta de entrada está vacía"})
    
    for filename in lista_imagenes:
        image_path = os.path.join(input_folder, filename)
        
        try:
            image_procesada = recortar_rostros(image_path)
            
            if image_procesada is not None:
                # Guardar
                img_name = f'procesada_{filename}'
                img_output_path = os.path.join(output_folder, img_name)
                cv2.imwrite(img_output_path, image_procesada)
        
        except Exception as e: 
            print(f"Error en {filename}: {str(e)}")
        
    return jsonify({"mensaje": "Imágenes procesadas y guardadas en la carpeta de salida"})