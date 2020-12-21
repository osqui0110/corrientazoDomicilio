# Tu corrientazo a domicilio
Este proyecto de pythn permite controlar rutas de drones de forma paralela mediante archivos de texto plano ubicados en
la carpeta orders.

El proyecto corre como script de python3.

## Para empezar a correr
- Instalar los requerimientos: pip3 install -r requirements.txt (Python 3)
- Asegurarse de que los archivos de texto en la carpeta reports se encuentren en el estado deseado
- Correr el script de python mediante: py delivery_starter.py

## Para correr pruebas unitarias
Correr el comando: pytest

## Para considerar
- Una vez creados los archivos de reportes, si el script es ejecutado, los nuevos resultados serán agregados a los 
archivos existentes.

- Si se desea generar reportes desde 0 simplemente se deben eliminar los archivos existentes de la carpeta.

- Durante la ejecución se cuenta con logs con salida a stdout.