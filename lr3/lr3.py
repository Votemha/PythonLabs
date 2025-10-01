import pprint
# Бинарное дерево
# Лабораторная 3

def userInputs():
    # Берем значения height и root от пользователя
    print("Генерация бинарного дерева")
    print("Для использования значений по умолчанию (height = 5, root = 1), оставьте поля пустыми.")
    height = input("Введите высоту дерева (height): ")
    root = input("Введите корень дерева (root): ")

    # Значения по умолчанию
    if height == "": height = 5  
    if root == "": root = 1

    # Проверка валидности
    if str(height).isdigit(): height = int(height)
    else: return("Значение height не целочисленно")
    if str(root).isdigit(): root = int(root)
    else: return("Значение root не целочисленно")
    
    return height, root

# Функция генерации бинарного дерева
def genBinTree(height, root):
    # Проверка валидности для тестов
    if str(height).isdigit(): height = int(height)
    else: return("Значение height не целочисленно")
    if str(root).isdigit(): root = int(root)
    else: return("Значение root не целочисленно")

    leftLeaf = root*2
    rightLeaf = root+3

    # Построение бинарного дерева
    return {
        root: root,
        f"left {leftLeaf}": genBinTree(height-1, leftLeaf) if height > 1 else None,
        f"right {rightLeaf}": genBinTree(height-1, rightLeaf) if height > 1 else None
    }

userFun = userInputs()

# Если ошибок не было
if len(userFun) == 2:
    # берем данные из функции usersDataInputs и вызываем функцию game
    userHeight, userRoot = userFun
    # pprint - выводит красиво дерево
    pprint.pprint(genBinTree(userHeight, userRoot))
else:
    # Если была найдена ошибка
    print(userFun)