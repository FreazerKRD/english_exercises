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

    ####### Сделать загрузку списка упражнений из бд
    
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
        # 60 - так как используются префиксы в callback query
        if len(exercise_sentence.split()) < 5 | len(exercise_sentence) > 60:
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
        
    # Генерация упражнения. Выделение фразы, требуется указать, какая это часть предложения
    # Упражнение еще не готово
    def exercise_noun_chunk(self, sentence: str) -> dict:
        exercise_sentence = sentence
        exercise_chunk = ''
        exercise_options = []
        exercise_answer = ''
        exercise_description = 'Какой частью предложения является выделенная фраза:'
        exercise_type = 'sentence_gen'

        # Выделение произвольных частей предложения
        for chunk in self.__nlp(exercise_sentence).noun_chunks:
            candidates.append(chunk)

        # Сохраняем порядок и выбираем случайные элементы. В тексте должно быть больше одного chunk
        if len(candidates) > 1:
            # Выберем случайный вариант из кандидатов
            winner = random.choise(candidates)
            
            exercise_chunk = exercise_sentence.replace(winner.text, '**'+winner.text+'**')
            exercise_answer = spacy.explain(chunk.root.dep_)
            candidates = winner.text
            task_options.append('')
            task_result.append('')

            # Возможные варианты ответа формируются из всех описаний части речи из task_answer
            # Если меньше 3-х вариантов ответа, то дозаполняем оставшиеся случайными значениями
            unique_answers = list(set(task_answer))
            dep_list = ['clausal modifier of noun (adjectival clause)', 'adjectival complement', 'adverbial clause modifier', 
                    'adverbial modifier', 'agent', 'adjectival modifier', 'appositional modifier', 'attribute', 'auxiliary', 
                    'auxiliary (passive)', 'case marking', 'coordinating conjunction', 'clausal complement', 'compound', 
                    'conjunct', 'copula', 'clausal subject', 'clausal subject (passive)', 'dative', 'unclassified dependent', 
                    'determiner', 'direct object', 'expletive', 'interjection', 'marker', 'meta modifier', 'negation modifier', 
                    'noun compound modifier', 'noun phrase as adverbial modifier', 'nominal subject', 'nominal subject (passive)', 
                    'object predicate', 'object', 'oblique nominal', 'complement of preposition', 'object of preposition', 
                    'possession modifier', 'pre-correlative conjunction', 'prepositional modifier', 'particle', 'punctuation', 
                    'modifier of quantifier', 'relative clause modifier', 'root', 'open clausal complement']
            for i in unique_answers:
                try:
                    dep_list.remove(i)
                except:
                    pass
            if len(unique_answers) == 2:
                unique_answers.append(random.choice(dep_list))
            elif len(unique_answers) == 1:
                unique_answers.extend(random.sample(dep_list, k=2))
            random.shuffle(unique_answers)
            task_options = [unique_answers for _ in task_options]
        else:
            task_object = np.nan
            task_options = np.nan
            task_answer = np.nan
            task_result = np.nan
            task_description = np.nan

        return {'raw' : text,
                'task_type' : task_type,
                'task_text' : task_text,
                'task_object' : task_object,
                'task_options' : task_options,
                'task_answer' : task_answer,
                'task_result' : task_result,
                'task_description' : task_description,
                'task_total': 0
                }