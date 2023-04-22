#bin/python3.7.9

from fastapi import FastAPI
from model.models import Corrector
from pydantic import BaseModel
import pandas as pd
from threading import Thread

app = FastAPI()

corpus = pd.read_csv("./model/corpus.csv")

@app.get('/correct/{word}')
async def index(word: str):
    corrector = Corrector(corpus=corpus, suggestion_limit=3)
    
    return {
        'word': word,
        'suggestions': corrector.correct(word),
    }

@app.get('/')
async def index():
    return {
        'test1': 'https://https://auto-correct-shakespear.onrender.com/correct/lofe',
        'test2': 'https://https://auto-correct-shakespear.onrender.com/correct/sam'
    }




if __name__ == "__main__":
    app.run()
    