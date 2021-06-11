import numpy as np
import random
import json
import pickle
import pathlib
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras import models

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

with open(pathlib.Path(__file__).parent/'model'/'chatbot'/'words.pkl', 'rb') as f:
    words = pickle.load(f)

with open(pathlib.Path(__file__).parent/'model'/'chatbot'/'classes.pkl', 'rb') as f:
    classes = pickle.load(f)

with open(pathlib.Path(__file__).parent/'model'/'chatbot'/'intents.json', 'rb') as f:
    intents = json.loads(f.read())

model: models.Model = models.load_model(pathlib.Path(__file__).parent/'model'/'chatbot'/'Chatbot.h5')


def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_TRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            return result
    return "Sorry , I can't understand You"


def robot(msg: str) -> str:
    """Input Question and Get Reply as Output"""
    ints = predict_class(msg)
    return str(get_response(ints, intents))


if __name__=='__main__':
    while True:
        message = input("User: ")
        res = robot(message)
        print(f"Bot: {res}")
