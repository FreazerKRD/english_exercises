import random
import spacy
import pyinflect
import en_core_web_sm
from decorator import timer
import gensim.downloader as api

class ExerciseGenerator:   
    def __init__(self) -> None:
        # Spacy medium
        self.__nlp = en_core_web_sm.load()
        # Glove wiki 100
        self.__glove = api.load("glove-wiki-gigaword-50")
        print('***Exercise generator started.***')

    # Функция для выбора упражнения по текущему предложению
    @timer
    def select_exercise(self, sentence: str) -> dict or None:
        exercises_list = [self.exercise_adjective_form(sentence),
                          self.exercise_verb_form(sentence),
                          self.exercise_sentence_gen(sentence)]
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
        exercise_type = 'adjective_form'
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
                'description' : exercise_description,
                'type' : exercise_type
                }
    
    # Генерация упражнения. Пропускает глагол с четырьмя формами для ответа.
    def exercise_verb_form(self, sentence: str) -> dict:
        exercise_sentence = sentence
        exercise_options = []
        exercise_answer = ''
        exercise_description = 'Выберите правильную форму глагола:'
        exercise_type = 'verb_form'
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
                'description' : exercise_description,
                'type' : exercise_type
                }
    
    # Генерация упражнения. Продолжает предложение с тремя сгенерированными вариантами.
    def exercise_sentence_gen(self, sentence: str) -> dict:
        exercise_sentence = sentence
        exercise_options = []
        exercise_answer = exercise_sentence
        exercise_description = 'Выберите правильное предложение:'
        exercise_type = 'sentence_gen'

        # Максимальная длина строки в Inline кнопке Telegram 64 байта
        # значит, при её превышении, или если слов меньше 5 - прерываем
        if len(exercise_sentence.split()) < 5 | len(exercise_sentence) > 63:
            return {}

        # Заменим существительные, глаголы, причастия и прилагательные
        # на случайные близкие слова и анти-слова
        new_sent_1, new_sent_2 = exercise_sentence, exercise_sentence
        i=3
        n_replaces = 0
        for token in self.__nlp(exercise_sentence):
            if n_replaces < 4 and token.pos_ in ['NOUN', 'VERB', 'ADV', 'ADJ'] and not token.is_stop:
                # Составим список похожих и противоположных слов
                synonyms = self.__glove.most_similar(token.text.lower(), topn=i)
                antonyms = self.__glove.most_similar(positive = [token.text.lower(), 'bad'],
                                                       negative = ['good'],
                                                       topn=i)

                # Выберем рандомные слова для замены
                new_words = []
                new_words.append(random.choice(synonyms)[0])
                new_words.append(random.choice(antonyms)[0])
                random.shuffle(new_words)
                
                # Сделать слова с заглавной буквы, если токен является таким
                new_words = [_.title() if token.text.istitle() else _ for _ in new_words]
                # Вставить слова в новые предложения
                new_sent_1 = new_sent_1.replace(token.text, new_words[0], 1)
                new_sent_2 = new_sent_2.replace(token.text, new_words[1], 1)

                n_replaces += 1

        if n_replaces > 1:
            exercise_options.extend([new_sent_1, new_sent_2, exercise_sentence])
            random.shuffle(exercise_options)
            return {'sentence' : exercise_sentence,
                    'options' : exercise_options,
                    'answer' : exercise_answer,
                    'description' : exercise_description,
                    'type' : exercise_type
                    }
        else:
            return {}