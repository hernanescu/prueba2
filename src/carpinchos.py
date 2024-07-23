import os 
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#   `
def concatenar_csvs(ruta):
    """Función que toma una carpeta y concatena csvs obtenidos de la API de Binance."""
    
    folder_path = ruta 
    dataframes = []

    for filename in os.listdir(folder_path): 
        if filename.endswith('.csv'): 
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path) 
            dataframes.append(df) 

    df_combined = pd.concat(dataframes, ignore_index=True)

    df_clean = df_combined.drop('Unnamed: 0', axis=1)
    df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], format='%Y%m%d%H%M%S')
    df_clean.sort_values(by='timestamp', inplace=True)
    df_clean.set_index('timestamp', inplace=True)

    return df_clean # el resultado es que te devuelve el df limpio

def preparar_data(data):
    """Función que realiza transformaciones sobre la serie de tiempo."""
    
    df = data.copy() 
    
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['second'] = df.index.second
    df['microsecond'] = df.index.microsecond
    df['nanosecond'] = df.index.nanosecond

    df['price_lag_1'] = df.groupby('symbol')['price'].shift(1)
    df['price_lag_2'] = df.groupby('symbol')['price'].shift(2)

    df['rolling_mean_2'] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(window=2).mean())
    df['rolling_std_2'] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(window=2).std())

    df['rolling_mean_3'] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(window=3).mean())
    df['rolling_std_3'] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(window=3).std())

    df['ema_3'] = df.groupby('symbol')['price'].transform(lambda x: x.ewm(span=3, adjust=False).mean())
    
    df['price_diff'] = df.groupby('symbol')['price'].diff()

    df['price_lag_1'] = df['price_lag_1'].ffill().bfill() 
    df['price_lag_2'] = df['price_lag_2'].ffill().bfill()
    df['price_diff'] = df['price_diff'].ffill().bfill()

    df['rolling_mean_2'] = df['rolling_mean_2'].fillna(df['rolling_mean_2'].mean())
    df['rolling_std_2'] = df['rolling_std_2'].fillna(df['rolling_std_2'].mean())
    df['rolling_mean_3'] = df['rolling_mean_3'].fillna(df['rolling_mean_3'].mean())
    df['rolling_std_3'] = df['rolling_std_3'].fillna(df['rolling_std_3'].mean())
    

    return df # devuelve el df procesado

def normalizar_crypto(data, crypto):
    """Función que realiza normalizaciones sobre la data de la criptomoneda elegida."""
    
    df = data.copy()

    if crypto == 'btc':
        subset_df = df[df['symbol'] == 'BTCUSDT']
        print("Subset de datos para Bitcoin (btc) listo.")

    elif crypto == 'eth':
        subset_df = df[df['symbol'] == 'ETHUSDT']
        print("Subset de datos para Ethereum (eth) listo.")
    
    else:
        raise ValueError(f"El valor '{crypto}' no es válido para 'crypto'. Debe ser 'eth' o 'btc'.")
    
    columns_to_normalize = ['price_lag_1', 'price_lag_2', 'rolling_mean_2', 'rolling_std_2', 'rolling_mean_3', 'rolling_std_3', 'ema_3', 'price_diff']

    scaler = StandardScaler() 
    # incorporamos lo que nos sugirio el warning
    subset_df.loc[:, columns_to_normalize] = scaler.fit_transform(subset_df[columns_to_normalize]) 
    
    print("Normalización lista.")
    return subset_df # devuelve el df listo y normalizado

def entrenar_modelo(data, persistir=False):
    """Función que entrena un modelo a partir de la criptomoneda elegida."""
    df = data.copy()

    # Vamos a emprolijar esta parte.
    # A esta altura, todavía no nos sacamos de encima la variable symbol, así que usémosla para marcar
    # a qué crypto aplica
    crypto_symbol = df['symbol'][0] # todos los valores son iguales, tomo el primero

    # Esta es la lista de variables con las que se entrenó, según vimos en todos los pasos anteriores
    variables_entrenamiento = ['hour', 'minute', 'second',
       'price_lag_1', 'price_lag_2', 'rolling_mean_2',
       'rolling_std_2', 'rolling_mean_3', 'rolling_std_3', 'ema_3',
       'price_diff']


    target = df['price']
    # Usamos la lista: en vez de decirle cuales queremos excluir, decimos cuáles queremos incluir
    features = df[variables_entrenamiento]

    # Dividimos en train y test
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Hagamos el famoso predict sobre los datos de prueba
    y_pred = model.predict(X_test)
    # evaluación del modelo
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Entrenamiento completo.')
    print(f'El modelo tuvo un MSE de {mse}.')
    print(f'El modelo tuvo un R2 de {r2}.')

    if persistir == True:
        # Existe la carpeta? Sino, la creamos.
        output_dir = 'models'
        os.makedirs(output_dir, exist_ok=True)
        # Aprovechamos la variable name para obtener el nombre del algoritmo
        nombre_algoritmo = type(model).__name__

        # Pegamos todo, agregando también el símbolo en cuestión
        path_modelo = f'{output_dir}/{crypto_symbol}-{nombre_algoritmo}.pkl'

        # Abrir el archivo en modo binario de escritura
        with open(path_modelo, 'wb') as archivo:
            # Serializar y guardar el objeto en el archivo
            pickle.dump(model, archivo)
        
            print(f'El modelo fue guardado en {path_modelo}')
    
    else:
        return model
