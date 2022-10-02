from sklearn.pipeline import Pipeline
from joblib import dump
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt 

# con esta sintaxis indicamos el tipo de dato de la variable de entrada (Type Pipeline) y de salida (type None)
def update_model(model: Pipeline) -> None: 
    dump(model, 'model/model.pkl')


def save_simple_metrics_report(train_score: float, test_score: float, validation_score: float, model: Pipeline) -> None:
    with open('report.txt', 'w') as report_file:# creamos un documento 

        report_file.write('# Model Pipeline Description')
        # dado que nuestro modelo es un pipeline esta compuesto de dos pasos, el ciclo for obtendra estos valores:
        ### imputer:SimpleImputer()
        ### core_model:GradientBoostingRegressor(n_estimators=180)
        for key, value in model.named_steps.items():
            report_file.write(f'### {key}:{value.__repr__()}'+'\n')

        report_file.write('### Train Score: {train_score}'+'\n') # ve a train.py para entender cada uno 
        report_file.write('### Test Score: {test_score}'+'\n')
        report_file.write('### Validation Score: {validation_score}'+'\n')

# graficamos el valor predicto y valor real
# los valores que se mueven de la diagonal son aquellos que el modelo no puede predecir bien 
def get_model_performance_test_set(y_real: pd.Series, y_pred: pd.Series) ->None:
    fig, ax = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(8)
    sns.regplot(x=y_pred, y=y_real, ax = ax)
    ax.set_xlabel('Predicted worldwide gross')
    ax.set_ylabel('Real worldwide gross')
    ax.set_title('Behavior of model prediction')
    fig.savefig('prediction_behavior.png') # se guarda el grafico en forma de imagen