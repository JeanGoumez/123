import cv2
from rembg import remove

MARGEN_ANCHURA = 0.20
MARGEN_ALTURA = 0.33
MARGEN_ALTURA_CABEZA = 0.15

def recortar_rostros(image_path):
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faces = face_cascade.detectMultiScale(image_gray)
    
    rostros = []


    for x, y, width, height in faces:
        widthreal = width * MARGEN_ANCHURA
        heightreal = height * MARGEN_ALTURA
        alturacabeza = int(height * MARGEN_ALTURA_CABEZA)
        posx = int(x - widthreal)
        posy = int(y - heightreal)
        widthend = int(width + (2*widthreal))
        heightend = int(height + (2*heightreal))

        if posx < 0:
            posx= 0
        if posy < 0:
            posy= 0
        if posx + widthend >  image.shape[1]:
            widthend= image.shape[1] - posx
        if posy + heightend + alturacabeza > image.shape[0]:
             heightend = image.shape[0] - posy
         

        imageOut = image[posy:posy+heightend+alturacabeza, posx:posx+widthend]
        imageOut_sinfondo = remove(imageOut,bgcolor=(255, 255, 255, 255))
        # cv2.imwrite(image_path, imageOut_sinfondo)
        # cv2.imwrite(image_path + "_2.jpg", imageOut)
        # image_recortada = imutils.resize(imageOut, height=image.shape[0])
        # imagen_concat = cv2.hconcat([image, image_recortada])
    
        rostro = {
            "dimensiones_imagen": {
                "ancho": int(image.shape[1]),
                "alto": int(image.shape[0])
            },
            # "rectangulo_rostro": {
            #     "x": int(x),
            #     "y": int(y),
            #     "ancho": int(width),
            #     "alto": int(height)
            # },
            # "rectangulo_recorte": {
            #     "x": int(posx),
            #     "y": int(posy),
            #     "ancho": int(posx+widthend),
            #     "alto": int(posy+heightend+alturacabeza)
            # }
        }
        
        return imageOut_sinfondo

    # Si no se encontraron rostros
    return None