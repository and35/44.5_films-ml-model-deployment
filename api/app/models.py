
# usando pydantic definiremos el tipo de dato que esperamos recibir de FastAPI
# esta sintaxis traduce del typado de fastAPI a el typado de python
from pydantic import BaseModel
# practicamente los definimos en una herencia(POO) de BaseModel 
class PredictionRequest(BaseModel):  
    opening_gross: float
    screens : float
    production_budget: float
    title_year: int
    aspect_ratio: float
    duration: int
    cast_total_facebook_likes: float
    budget: float
    imdb_score: float

class PredictionResponse(BaseModel):
    worldwide_gross: float