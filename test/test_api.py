# si no se encuentra api.main ejecuta esto 
#import sys
#sys.path.append('../')

from fastapi.testclient import TestClient  #importamos testing de FA
#app_FA_path = os.environ.get('app_FAST','../app/main.py')
from api.main import app    # importamos la app a testear

client = TestClient(app) # con esto podremos usar la API desde este archivo sin necesidad de la UI de uvicorn 

# creamos las funciones de testing 

# una para revisar que el modelo responde ante un input en ceros que da FA por default 
def test_null_prediction():
    response = client.post('/v1/prediction', json = { # usamos el metodo http con el endpoint de la app al que queremos acceder
                                                    'opening_gross': 0,
                                                    'screens': 0,
                                                    'production_budget': 0,
                                                    'title_year': 0,
                                                    'aspect_ratio': 0,
                                                    'duration': 0,
                                                    'cast_total_facebook_likes': 0,
                                                    'budget': 0,
                                                    'imdb_score': 0
                                                    })
    # analizamos la respuesta del servidor                                            
    assert response.status_code == 200  # 200 = operacion succesfull 
    assert response.json()['worldwide_gross'] == 0 # el resultado es un json evaluamos que la respuesta sea = 0


# hacemos otra prueba ahora con una muestra real  del dataset. seguimos la logica de arriba
def test_random_prediction():
    response = client.post('/v1/prediction', json = {
                                                    'opening_gross': 8330681,
                                                    'screens': 2271,
                                                    'production_budget': 13000000,
                                                    'title_year': 1999,
                                                    'aspect_ratio': 1.85,
                                                    'duration': 97,
                                                    'cast_total_facebook_likes': 37907,
                                                    'budget': 16000000,
                                                    'imdb_score': 7.2
                                                })
    assert response.status_code == 200
    assert response.json()['worldwide_gross'] != 0 