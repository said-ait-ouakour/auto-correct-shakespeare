
from fastapi import FastAPI
from model.models import Corrector
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

corpus = pd.read_csv("./model/corpus.csv")

@app.get('/correct/{word}')
async def index(word: str):
    corrector = Corrector(corpus=corpus, suggestion_limit=3)
    
    return {
        'word': word,
        'suggestions': corrector.correct(word),
    }
    
    