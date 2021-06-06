import pickle
import pathlib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from typing import Union, Dict
from pydantic import BaseModel


class Covi_Tracker(BaseModel):
    breathing_problem: bool
    fever: bool
    dry_cough: bool
    sore_throat: bool
    abroad_travel: bool
    contact_with_covid_patient: bool
    attended_large_gathering: bool


with open(pathlib.Path(__file__).parent/'ML-integrations22'/'Covid Checker'/'checker.pkl', 'rb') as file:
    '''Loads Saved Model during Import'''
    model: LogisticRegression = pickle.load(file)


def format_mapper(input: Covi_Tracker) -> dict:
    return {
        'Breathing Problem' : [int(input.breathing_problem)],
        'Fever' : [int(input.fever)],
        'Dry Cough' : [int(input.dry_cough)], 
        'Sore throat' : [int(input.sore_throat)],
        'Abroad travel' : [int(input.abroad_travel)], 
        'Contact with COVID Patient' : [int(input.contact_with_covid_patient)],
        'Attended Large Gathering' : [int(input.attended_large_gathering)]
    }


def predict(data: Union[Dict, Covi_Tracker]) -> float:
    '''Predicts the chance of being covid positive'''
    if isinstance(data, Covi_Tracker): data: dict = format_mapper(data)
    data: pd.DataFrame = pd.DataFrame.from_dict(data)
    return model.predict_proba(data)[0][1]


# DEBUG

if __name__=='__main__':
    test_data = {
        'Breathing Problem' : [1],
        'Fever' : [0],
        'Dry Cough' : [0], 
        'Sore throat' : [1],
        'Abroad travel' : [1], 
        'Contact with COVID Patient' : [1],
        'Attended Large Gathering' : [0]
    }
    print("Your COVID-19 prabability is", predict(test_data)*100, "%")