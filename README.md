# Microservicio recorte de IMAGEN

Este repositorio sirve para que automaticamente haga el recorte de la imagen haciendo un llamado a REST tipo POST.

## Versiones

python version 3.10.11

## Instalación de paquetes necesarios

Instalamos Flask, request y opencv

```py
pip install Flask
pip install requests
pip install opencv-python
```

## Funcionamiento

Para hacerlo correr ejedutamos el comando:

```bash
flask --app app --debug  run
```

Esto hara que podamos usar la aplicacion en el puerto 5000, para hacerlo funcionar usamos postman y enviamos los siguientes valores

## Api Rest

Enviar mediante postman o curl el siguiente body:

```bash
curl --location 'http://127.0.0.1:5000/procesar_imagen' \
--header 'Content-Type: application/json' \
--data '{
    "url_imagen": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg"
}'
```

Nos retorara lo siguiente:

```json
{
  "rostros": [
    {
      "dimensiones_imagen": {
        "alto": 1480,
        "ancho": 1080
      },
      "rectangulo_recorte": {
        "alto": 1291,
        "ancho": 1013,
        "x": 88,
        "y": 95
      },
      "rectangulo_rostro": {
        "alto": 661,
        "ancho": 661,
        "x": 221,
        "y": 314
      }
    }
  ]
}
```

Autores:
@JeanGoumez
