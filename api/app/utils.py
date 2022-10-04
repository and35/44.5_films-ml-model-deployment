#from pickle import load  # pickle carga el modelo como un array de numpy 
from joblib import load 
from scipy.sparse import data
from sklearn.pipeline import Pipeline
from pydantic import BaseModel
from pandas import DataFrame
import os 
from io import BytesIO

#cargamos el modelo en 1 linea :)
# sacado de aqui https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
def get_model() -> Pipeline: # creamos una funcion sin parametros que retornara un objeto de tipo Pipeline 
    model = load("model/model.pkl")
    return model

"""def get_model_2_no_sirvio_esta_funcion() -> Pipeline: # creamos una funcion sin parametros que retornara un objeto de tipo Pipeline 
    # definimos una variable de entorno de python que contenga el path del modelo 
    model_path = os.environ.get('MODEL_PATH','model/model.pkl') 
    with open(model_path,'rb') as model_file:  # debemos abrimos el archivo del modelo usando la variable de entorno  
        # leemos el contenido del archivo y lo pasamos de bites a str
        # de esta forma ya lo podemos cargar ahora si usando joblib 
        model = load(BytesIO(model_file.read()))  
    return model"""

# esta funcion recibira lo que demos de entrada a la vista de FastAPI y la convertira en DF
def transform_to_dataframe(class_model: BaseModel) -> DataFrame:
    # Fast API recibe el input en forma de json nosotros lo transformaremos en un diccionario 
    # con la forma de {key: [value], key: [value]} despues pasamos a DF
    transition_dictionary = {key:[value] for key, value in class_model.dict().items()}
    data_frame = DataFrame(transition_dictionary)
    return data_frame
