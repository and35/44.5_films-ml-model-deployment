from fastapi import FastAPI
from .app.models import PredictionResponse, PredictionRequest
from .app.views import get_prediction

app = FastAPI(docs_url='/')

@app.post('/v1/prediction') # creamos una vista  
def make_model_prediction(request: PredictionRequest): # la vista esperara request de tipo PredictionRequest
    return PredictionResponse(worldwide_gross=get_prediction(request))


    