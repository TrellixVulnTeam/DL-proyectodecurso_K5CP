import os, spacy, pickle
import numpy as np
from time import time
from torchtext import data
from torchtext import datasets

def load_anki_dataset(path):
    spacy_es = spacy.load('es')
    spacy_en = spacy.load('en')

    def tokenize_es(text):
        return [tok.text for tok in spacy_es.tokenizer(text)]

    def tokenize_en(text):
        return [tok.text for tok in spacy_en.tokenizer(text)]

    ES = data.Field(tokenize=tokenize_es, lower=True)
    EN = data.Field(tokenize=tokenize_en, lower=True,
                    init_token='<sos>', eos_token='<eos>')

    with open(path, 'rb') as f:
        examples = pickle.load(f)

    dataset = data.Dataset(examples, [('en', EN), ('es', ES)])

    ES.build_vocab(dataset.es)
    EN.build_vocab(dataset.en)

    return dataset, ES, EN