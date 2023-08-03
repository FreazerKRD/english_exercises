from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def books_kb(posts, n): # Передаем массив всех rybu и желаемый индекс последнего выводимого товара
    books_kb = InlineKeyboardMarkup()
    for i in range(n-10, len(posts)): # Так как я решил выводить только 10 позиций за раз, то от конечного индекса отнимаем 10
        if i >= n or i > len(posts): #Проверка на то когда нужно прекращать добавлять кнопки(когда индекс больше передаваемого, чтобы не выводилось больше позиций чем нужно. И проверка на то, если у последней страницы не хватает "добить" 10 позиций, оно не крашилось изза выхода за пределы массива)
            break
        else:
            current = InlineKeyboardButton(str(posts[i][1]), callback_data=posts[i][0])#Создаю кнопку в тексте которой название книги, а в callback_data закидываю id книги из бд для дальнейшего взаимодействия
            books_kb.add(current) # Добавляю в клавиатуру
    if n <= 10 and n >= len(posts):#Здесь идут проверки для добавления кнопок назад/вперед чтобы в конце списка не появлялась кнопка вперед
        cancel = InlineKeyboardButton("Отмена", callback_data="cancel_offers")
        books_kb.row(cancel)
    elif n == 10:
        forward = InlineKeyboardButton("Вперед", callback_data = "forward_offers" )
        cancel = InlineKeyboardButton("Отмена", callback_data="cancel_offers")
        books_kb.row(forward)
        books_kb.row(cancel)
    elif n>=len(posts):
        back= InlineKeyboardButton("Назад", callback_data="back_offers" )
        cancel = InlineKeyboardButton("Отмена", callback_data="cancel_offers")
        books_kb.row(back)
        books_kb.row(cancel)
    else:
        forward = InlineKeyboardButton("Вперед", callback_data = "forward_offers" )
        back= InlineKeyboardButton("Назад", callback_data="back_offers" )
        cancel = InlineKeyboardButton("Отмена", callback_data="cancel_offers")
        books_kb.row(back, forward)
        books_kb.row(cancel)
    return books_kb 