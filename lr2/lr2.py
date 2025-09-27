import random

# игровая функция
print("Игра 'Угадай число'")
# Функция, которая принимает данные от пользователя 
# (загаданное число, диапазон угадываения)
def usersDataInputs():

    # Принимаем число от пользователя, которое нужно угадать
    guessNumberStr = input("Введите число для начала игры: ")
    # Проверка валидности числа
    if not (guessNumberStr.lstrip('-').isdigit() and guessNumberStr != '-'):
        return "Значение загаданного числа не целочисленно"
    guessNumber = int(guessNumberStr)

    '''
        Принимаем диапазон, в котором загадано число
        rangeUserMin - начало диапазона
        rangeUserMin - конец диапазона
    '''
    rangeUserMin, rangeUserMax = map(int, input("Введите два значения через пробел, в диапазон между которыми входит ваше число (первое - начало диапазона, второе - конец): ").split(" "))
    if not isinstance(rangeUserMin, int): return "Значение загаданного диапазона не целочисленно"
    if not isinstance(rangeUserMax, int): return "Значение загаданного диапазона не целочисленно"
    if rangeUserMin >= rangeUserMax: return "Начало диапазона не может быть больше или равно концу диапазона"
    

    '''
        Заполняем список рандомными числами
        Цикл берет 300 чисел
        lst - список рандомных чисел в заданном диапазоне
    '''
    lst = []
    for i in range(1, 10+1):
        # Генерим рандомное число в заданном диапазоне
        lst.append(random.randint(rangeUserMin, rangeUserMax))
    # Убираем повторы и сортируем список
    lstSorted = list(sorted(set(lst)))
    print("Список рандомных чисел в диапазоне:", lstSorted)

    return guessNumber, lstSorted

''' 
    Функция, которая реализует игру 'Угадай число'
    На вход принимает загаданное число и список чисел
    Возвращает само число и количество попыток, за которое оно было угадано
    Например:
    Входные данные:
    5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Выходные данные:
    "Загаданное число: 5, найдено за 1 попыток"
'''
def game(guessNumber, lstSorted):

    # Проверки валидности
    if not isinstance(guessNumber, int): return "Значение загаданного числа не целочисленно"

    '''
        Реализуем бинарный поиск
        LBorder - левая граница поиска
        RBorder - правая граница поиска
    '''
    LBorder, RBorder = 0, len(lstSorted) - 1
    # Счетчик попыток
    count = 0
    while LBorder <= RBorder:
        # увеличиваем счетчик попыток
        count += 1

        # Находим середину списка
        midValue = (LBorder + RBorder) // 2
        # Если число в середине списка равно загаданному числу
        if lstSorted[midValue] == guessNumber: return(f"Загаданное число: {guessNumber}, найдено за {count} попыток")
        # Если загаданное число больше числа в середине
        elif lstSorted[midValue] < guessNumber: LBorder = midValue + 1
        # Если загаданное число меньше числа в середине
        else: RBorder = midValue - 1

    else:
        # Если число не найдено
        return None

userGuess = usersDataInputs()

if len(userGuess) == 2:
    # берем данные из функции usersDataInputs и вызываем функцию game
    userFGuessNumber, userFLstSorted = userGuess
    print(game(userFGuessNumber, userFLstSorted))
else:
    # Если была найдена ошибка
    print(userGuess)