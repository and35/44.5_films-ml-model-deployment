from .models import PredictionRequest
from .utils import get_model, transform_to_dataframe

model = get_model()

def get_prediction(request: PredictionRequest) -> float:
    data_to_predict = transform_to_dataframe(request)
    prediction = model.predict(data_to_predict)[0]# esto es un array y solo queremos el primer valor 
    return max(0, prediction) # devuelve el mayor de los 2 valores
# nunca hay que entregar una prediccion cruda a un usuario final hay que tratarla. con el max evitamos valores negativos