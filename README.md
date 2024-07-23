# PAECIS: Proyecto final

## Introducción
Este es el repositorio de la cuarta clase de PAECIS.

El proyecto toma datos obtenidos de la API de Binance y entrena un modelo de regresión logística con el objetivo de predecir el precios de la moneda.

### Setup
Dentro del código se encuentra el paquete realizado para efectuar las operaciones. 

Dentro de un ambiente nuevo (Conda/venv), a nivel de root, debe ejecutarse `pip install .` para instalar todo el código necesario, desde los requerimientos generales hasta el código fuente final.

El paquete `carpinchos` tiene las cuatro funciones autogeneradas, y están disponibles en el entorno para ser utilizadas en contexto de I+D.

### Ejecutar via CLI
Una vez instalado el paquete, para ejecutar punta a punta, el `main.py` requiere la ruta hacia los archivos crudos, asignada vía la variable `--path`, y la elección de la criptomoneda. 

Al momento, el programa permite elegir `btc` (bitcoin) y `eth` (ethereum).  

Existe un flag opcional llamado `--persistir`, que permite guardar el modelo en formato `.pkl`.

#### Ejemplo
`python3 main.py --crypto=btc --path="data/raw" --persistir`

