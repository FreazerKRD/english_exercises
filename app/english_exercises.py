#import os
#import re
import pandas as pd
import numpy as np
import random
import spacy
import en_core_web_md
import pyinflect
#import gensim.downloader as api

class ExerciseGenerator:
    def __init__(self) -> None:
        # Spacy medium
        self.__nlp = en_core_web_md.load()
        # Glove wiki 100
        # self.__glove = api.load("glove-wiki-gigaword-100")

    # Генерация упражнения. Пропускает прилагательное с тремя степенями для ответа.
    def exercise_adjective_form(self, sentence):
        exercise_sentence = sentence
        #exercise_objects = []
        exercise_options = []
        exercise_answer = ''
        exercise_type = 'adjective_form'
        exercise_description = 'Выберите правильную форму прилагательного:'
        candidates = []

        # Изменение формы прилагательного
        for token in self.__nlp(sentence):
            # Выбор прилагательных для которых есть все 3 степени сравнения
            if (token.pos_=='ADJ' and 
                token._.inflect('JJ') != None and 
                token._.inflect('JJR') != None and 
                token._.inflect('JJS') != None):
                candidates.append(token)
        if candidates != []:
            # Выбираем случайный объект из списка кандидатов и заполняем параметры упражнения
            winner = random.choice(candidates)
            exercise_answer = winner.text
            exercise_sentence = exercise_sentence.replace(winner.text, '_____')
            exercise_options.append(winner._.inflect('JJ'))  # Adjective Positive
            exercise_options.append(winner._.inflect('JJR')) # Adjective comparative
            exercise_options.append(winner._.inflect('JJS')) # Adjective superlative
            # Перемешаем ответы для разного порядка
            random.shuffle(exercise_options)
        else:
            # Если нет подходящих кандидатов - прерываем цикл
            return False
        return {'type' : exercise_type,
                'sentence' : exercise_sentence,
                'options' : exercise_options,
                'answer' : exercise_answer,
                'description' : exercise_description
                }

    