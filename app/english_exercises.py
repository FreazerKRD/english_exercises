#import os
#import re
import pandas as pd
import numpy as np
import random
import spacy
import en_core_web_md
import pyinflect
from decorator import timer
#import gensim.downloader as api

class ExerciseGenerator:   
    def __init__(self) -> None:
        # Spacy medium
        self.__nlp = en_core_web_md.load()
        # Glove wiki 100
        # self.__glove = api.load("glove-wiki-gigaword-100")
        print('***Exercise generator started.***')

    # Функция для выбора упражнения по текущему предложению
    @timer
    def select_exercise(self, sentence: str) -> dict:
        exercises_list = [self.exercise_adjective_form(sentence),
                          self.exercise_verb_form(sentence)]
        random.shuffle(exercises_list)
        while exercises_list:
            result = exercises_list[0]
            if result:
                return result
            else:
                del exercises_list[0]
        return result

    # Генерация упражнения. Пропускает прилагательное с тремя степенями для ответа.
    def exercise_adjective_form(self, sentence: str) -> dict:
        exercise_sentence = sentence
        exercise_options = []
        exercise_answer = ''
        exercise_description = 'Выберите правильную форму прилагательного:'
        candidates = []

        # Изменение формы прилагательного
        for token in self.__nlp(sentence):
            # Выбор прилагательных для которых есть все 3 степени сравнения
            if (token.pos_=='ADJ' and 
                token._.inflect('JJ') != None and 
                token._.inflect('JJR') != None and 
                token._.inflect('JJS') != None and
                token not in candidates):
                candidates.append(token)
        if candidates != []:
            # Выбираем случайный объект из списка кандидатов и заполняем параметры упражнения
            winner = random.choice(candidates)
            exercise_answer = winner.text
            exercise_sentence = exercise_sentence.replace(winner.text, '_____', 1)
            exercise_options.append(winner._.inflect('JJ'))  # Adjective Positive
            exercise_options.append(winner._.inflect('JJR')) # Adjective comparative
            exercise_options.append(winner._.inflect('JJS')) # Adjective superlative
            # Перемешаем ответы для разного порядка
            random.shuffle(exercise_options)
        else:
            # Если нет подходящих кандидатов - прерываем цикл
            return {}
        return {'sentence' : exercise_sentence,
                'options' : exercise_options,
                'answer' : exercise_answer,
                'description' : exercise_description
                }
    
    # Генерация упражнения. Пропускает глагол с четырьмя формами для ответа.
    def exercise_verb_form(self, sentence: str) -> dict:
        exercise_sentence = sentence
        exercise_options = []
        exercise_answer = ''
        exercise_description = 'Выберите правильную форму глагола:'
        candidates = []

        # Формы глаголов
        verb_forms = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        random.shuffle(verb_forms)
        
        # Выберем все глаголы
        for token in self.__nlp(sentence):
            if token.pos_=='VERB' and token not in candidates:
                candidates.append(token)

        if candidates != []:
            # Выбираем случайный объект из списка кандидатов и заполняем параметры упражнения
            winner = random.choice(candidates)
            exercise_answer = winner.text
            exercise_sentence = exercise_sentence.replace(winner.text, '_____', 1)
            exercise_options.append(winner.text)
            for i in verb_forms:
                if (winner._.inflect(i) != None and 
                    winner._.inflect(i) not in exercise_options):
                    exercise_options.append(winner._.inflect(i))
            exercise_options = exercise_options[:4]

            # Перемешаем ответы для разного порядка
            random.shuffle(exercise_options)
        else:
            # Если нет подходящих кандидатов - прерываем цикл
            return {}
        return {'sentence' : exercise_sentence,
                'options' : exercise_options,
                'answer' : exercise_answer,
                'description' : exercise_description
                }