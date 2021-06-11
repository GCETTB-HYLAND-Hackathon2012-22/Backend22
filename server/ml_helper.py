import pickle
import pathlib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from typing import Union, Dict
from pydantic import BaseModel


class Medi_Checker(BaseModel):
    breathing_problem: Union[int, bool] = 0
    fever: Union[int, bool] = 0
    dry_cough: Union[int, bool] = 0
    sore_throat: Union[int, bool] = 0
    abroad_travel: Union[int, bool] = 0
    contact_with_covid_patient: Union[int, bool] = 0
    attended_large_gathering: Union[int, bool] = 0


with open(pathlib.Path(__file__).parent/'model'/'checker.pkl', 'rb') as file:
    '''Loads Saved Model during Import'''
    model: LogisticRegression = pickle.load(file)


def format_mapper(input: Medi_Checker) -> dict:
    return {
        'Breathing Problem' : [int(input.breathing_problem)],
        'Fever' : [int(input.fever)],
        'Dry Cough' : [int(input.dry_cough)], 
        'Sore throat' : [int(input.sore_throat)],
        'Abroad travel' : [int(input.abroad_travel)], 
        'Contact with COVID Patient' : [int(input.contact_with_covid_patient)],
        'Attended Large Gathering' : [int(input.attended_large_gathering)]
    }


def predict(data: Union[Dict, Medi_Checker]) -> float:
    '''Predicts the chance of being covid positive'''
    if isinstance(data, Medi_Checker): data: dict = format_mapper(data)
    data: pd.DataFrame = pd.DataFrame.from_dict(data)
    return model.predict_proba(data)[0][1]


# DEBUG

if __name__=='__main__':
    test_data = format_mapper(Medi_Checker(
        breathing_problem=False, fever=True, dry_cough=True, sore_throat=False, abroad_travel=True,
        contact_with_covid_patient=False, attended_large_gathering=False
    ))
    print("Your COVID-19 prabability is", predict(test_data)*100, "%")