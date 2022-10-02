from dvc import api # nos permite usar dvc con codigo de python 
import pandas as pd
from io import StringIO # pasa los archivos de formato nativo de bites a un objeto str (los que maneja pandas)
import sys
import logging

from pandas.core.tools import numeric

#Logging es un medio de rastrear los eventos que ocurren cuando se ejecuta algún software, y asi poder registrarlos 
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s', # esto es lo que se mstrara en consola
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

logging.info('Fetching data...')

# cargamos los dataset desde el almacenamiento remoto (Gdrive) especificado en dvc
movie_data_path = api.read('dataset/movies.csv', remote='dataset-track', encoding="utf8") # nos ahorramos el movies.csv.dvc ya que el .dvc esta explicito
finantial_data_path = api.read('dataset/finantials.csv', remote='dataset-track', encoding="utf8")
opening_data_path = api.read('dataset/opening_gross.csv', remote='dataset-track', encoding="utf8")

# aqui hacemos el data engenering como en el notebook moodeling 
fin_data = pd.read_csv(StringIO(finantial_data_path))
movie_data = pd.read_csv(StringIO(movie_data_path))
opening_data = pd.read_csv(StringIO(opening_data_path))

numeric_columns_mask = (movie_data.dtypes == float) | (movie_data.dtypes == int)
numeric_columns = [column for column in numeric_columns_mask.index if numeric_columns_mask[column]]
movie_data = movie_data[numeric_columns+['movie_title']]

fin_data = fin_data[['movie_title', 'production_budget', 'worldwide_gross']]

fin_movie_data = pd.merge(fin_data, movie_data, on='movie_title', how='left')
full_movie_data = pd.merge(opening_data, fin_movie_data, on='movie_title', how='left')

full_movie_data = full_movie_data.drop(['gross','movie_title'], axis=1)

full_movie_data.to_csv('dataset/full_data.csv',index=False)
# al final tenemos un dataset limpio y guardado en formato csv listo para usar por el modelo
#breackpoint()
logger.info('Data Fetched and prepared...')