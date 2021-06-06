import pickle
import pathlib
import pandas as pd
from sklearn.linear_model import LogisticRegression

with open(pathlib.Path(__file__).parent/'ML-integrations22'/'Covid Checker'/'checker.pkl', 'rb') as file:
    '''Loads Saved Model during Import'''
    model: LogisticRegression = pickle.load(file)


def predict(data: dict) -> float:
    '''Predicts the chance of being covid positive'''
    data = pd.DataFrame.from_dict(data)
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