import click
from src.carpinchos import * 

# dos observaciones
# 1 - le indico src. antes, porque el main va a estar alojado a nivel de root de proyecto. El codigo tiene que
# ir a la carpeta donde está el .py e importarse. Es distinto a la notebook porque no está instalado en el entorno
# 2 - con import * importamos todas las funciones

@click.command()
@click.option('--crypto', type=click.Choice(['btc', 'eth']), required=True, help='La criptomoneda elegida. Los valores permitidos son eth o btc.')
@click.option('--path', type=click.Path(exists=True), required=True, help="Ruta hacia la carpeta donde están los CSVs.")
@click.option('--persistir', is_flag = True, help="Opcional: permite persistir el modelo creado.")


def main(crypto, path, persistir):
    """Programa en Python que entrena una regresión logística a partir de datos de la API de Binance."""
    df_concatenado = concatenar_csvs(path)
    df_preparado = preparar_data(df_concatenado)
    df_eth_normalizado = normalizar_crypto(df_preparado, crypto)
    entrenar_modelo(df_eth_normalizado, persistir=persistir)
    click.echo('Proceso completo.')
    

if __name__ == "__main__":
    main()
