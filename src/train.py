from model_utils import update_model, save_simple_metrics_report, get_model_performance_test_set
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor

import logging
import sys
import numpy as np
import pandas as pd

# 1 definimos un logger que nos muestre el avance del codigo en cada fase 
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# 2 cargamos la data ya lista 
logger.info('Loading Data...')
data = pd.read_csv('dataset/full_data.csv')


logger.info('Loading model...')
# 3 definimos un pipeline: arreglador de valores null + modelo 
model = Pipeline([
    ('imputer', SimpleImputer(strategy='mean',missing_values=np.nan)),
    ('core_model', GradientBoostingRegressor())
])

# 4 definimos X y Y y hacemos el holdout(split)
logger.info('Seraparating dataset into train and test')
X = data.drop(['worldwide_gross'], axis= 1)
y = data['worldwide_gross']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

# 5 hacemos el ajuste de hiperparametros y entrenamiento al mismo tiempo
#       a) definimos el parametro y rango a testear 
logger.info('Setting Hyperparameter to tune')
param_tuning = {'core_model__n_estimators':range(20,301,20)}

grid_search = GridSearchCV(model, param_grid= param_tuning, scoring='r2', cv=5)

#       b) aqui iniciamos el entrenamiento de varios modelos con diferentes parametros
logger.info('Starting grid search...')
grid_search.fit(X_train, y_train)

# 6 evaluamos el mejor modelo haciendo cross validation
logger.info('Cross validating with best model...')
# ten en cuenta que estamos evaluando con el 20% del dataset de entrenamiento 
final_result = cross_validate(grid_search.best_estimator_, X_train, y_train, return_train_score=True, cv=5)
#       a) obtenemos el promedio de las metricas
train_score = np.mean(final_result['train_score'])
test_score = np.mean(final_result['test_score'])
assert train_score > 0.7 
assert test_score > 0.65

logger.info(f'Train Score: {train_score}') # las mostramos usando logger
logger.info(f'Test Score: {test_score}')

# 7 el mejor modelo que acabamos de escoger sera el que guardaremos 
logger.info('Updating model...')
update_model(grid_search.best_estimator_) # funcion en utils.py

#8 hacemos la evaluacion ahora con data nunca vista 
logger.info('Generating model report...')
validation_score = grid_search.best_estimator_.score(X_test, y_test)
save_simple_metrics_report(train_score, test_score, validation_score, grid_search.best_estimator_)
""" es importante diferenciar las 3 metricas: 
    - train_score y test_score: se obtienen del cross validation. 
        se hacen con el 80%(conocido) y 20%(desconocido) del dataset test 
    - validation_score: con los datos del split. datos nunca vistos. son el 35% del dataset total
"""

y_test_pred = grid_search.best_estimator_.predict(X_test)
get_model_performance_test_set(y_test, y_test_pred)

logger.info('Training Finished')

