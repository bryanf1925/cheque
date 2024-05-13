from django.shortcuts import render
from .form import UploadFileForm
from .load import extraxt_digit_from_image,segmentar_imagen, predecirNumero, dividirDigitos
import numpy as np
import base64
#from django.http import HttpResponse
import cv2
# Create your views here.
#muestrame el hola mundo con https
 
def index(request):
 
    if request.method == 'POST':
        formulario = UploadFileForm(request.POST, request.FILES)
        if formulario.is_valid():
            image_bytes = request.FILES['Image'].file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            im=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #digit = extraxt_digit_from_image(image_bytes)
            digitos = segmentar_imagen(im)
            digitosDivididos=dividirDigitos(digitos)
            numero= predecirNumero(digitosDivididos)
            _, digitos_buffer = cv2.imencode('.png', digitos)
            digitos_base64 = base64.b64encode(digitos_buffer).decode('utf-8')
            return render(request, 'index.html', {'formulario': formulario, 'roi':digitos_base64,'digitos': digitosDivididos, 'numero': numero})
    else:
        formulario = UploadFileForm()
        return render(request, 'index.html', {'formulario': formulario})