from keras.models import load_model
from PIL import Image
import numpy as np
import io
import cv2
import base64
import matplotlib.pyplot as plt
def segmentar_imagen(image_bytes):
    im1=cv2.resize(image_bytes, (1496, 596))
    alto, ancho, _ = im1.shape
    print('alto',alto,'amcho', ancho)
    im2 = im1[int (alto/5):int ((alto*2)/(6)),int ((ancho*3)/4):int(ancho)]
    print('la imagen es',im2)
    return im2
def dividirDigitos(im2):
    region_gris = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    _, region_binaria = cv2.threshold(region_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contornos, _ = cv2.findContours(region_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=lambda x: cv2.boundingRect(x)[0]) 
    digitos = []
    for contorno in contornos:
    # Obtener las coordenadas del rectángulo que rodea al contorno
        x, y, w, h = cv2.boundingRect(contorno)
                # Recortar la región del dígito
        margen = 1  # Puedes ajustar este margen según sea necesario
        x -= margen
        y -= margen
        w += 2 * margen
        h += 2 * margen
        digito = region_gris[y:y+h, x:x+w]
                # Asegurarse de que el dígito tenga un tamaño mínimo (ajustar según sea necesario)
        if w > 15 and h > 15:
                    # Agregar el dígito a la lista de dígitos
            digitos.append(digito)
    digitos_codificados = []
    for digito in digitos:
        _, buffer = cv2.imencode('.png', digito)
        base64_data = base64.b64encode(buffer).decode('utf-8')
        digitos_codificados.append(base64_data)
    return digitos_codificados

    
def predecirNumero(digitos):
    numeros=""
    for digito in digitos:
        bytes_data = base64.b64decode(digito)
        numeros +=str( extraxt_digit_from_image(bytes_data) ) # No es necesario convertir a bytes nuevamente
    print('el numero es ',numeros)
    return numeros
def extraxt_digit_from_image(image_bytes):
   
    model = load_model('app/modelo_mnist.h5')
   
    # Convertir la imagen a escala de grises
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    # Cambiar el tamaño de la imagen
    image = image.resize((28, 28))
    # Convertir la imagen a un arreglo de numpy
    image = np.array(image)
    # Normalizar la imagen
    image = image / 255
    # Cambiar la forma de la imagen
    image = image.reshape(1, 28, 28, 1)
    # Realizar la predicción
    prediction = model.predict([image])
    # Obtener el dígito predicho
    digit = np.argmax(prediction)
    return digit
