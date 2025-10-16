'''
Функция для генерации бинарного дерева нерекурсивным методом
На вход принимает: 
высоту дерева, значение корня, функции для генерации левого и правого потомка
На выходе возвращает дерево в виде вложенных словарей
'''
def gen_bin_tree(height=5, root=1, leftBranch=lambda x: x*2, rightBranch=lambda y: y+3):
    if not callable(leftBranch) or not callable(rightBranch):
        return "Функции должны быть callable"
    elif str(height).isdigit() == False or str(root).isdigit() == False:
        return "Значения height и root должны быть целочисленными"
    elif height < 1:
        return "Высота дерева должна быть больше 0"

    # Задаем корень дерева
    tree = {'value': root, 'left': None, 'right': None}

    # Стек хранения узлов дерева
    stack = [(tree, 0)]

    # Основной цикл реализации дерева
    while stack:
        # получаем значения узела и уровеня дерева
        node, level = stack.pop()

        if level < height:
            '''
            Левая ветвь:
            Получаем значение левой ветви, 
            если оно не None, то создаем узел,
            добавляем его в дерево
            '''
            leftValue = leftBranch(node['value'])
            if leftValue is not None:
                leftNode = {'value': leftValue, 'left': None, 'right': None}
            else:
                leftNode = None
            node['left'] = leftNode

            '''
            Правая ветвь:
            Получаем значение правой ветви, 
            если оно не None, то создаем узел,
            добавляем его в дерево
            '''
            rightValue = rightBranch(node['value'])
            if rightValue is not None:
                rightNode = {'value': rightValue, 'left': None, 'right': None}
            else:
                rightNode = None
            node['right'] = rightNode

            if leftBranch and level + 1 < height:
                stack.append((leftNode, level + 1))
            if rightBranch and level + 1 < height:
                stack.append((rightNode, level + 1))
    
    return tree

# Функция печати дерева
def print_tree(func):
    stack = [(func, 0)]
    while stack:
        node, level = stack.pop()
        # Печатаем значение узла с отступом в зависимости от уровня
        print("  " * level + str(node['value']))
        if node['right']:
            stack.append((node['right'], level + 1))
        if node['left']:
            stack.append((node['left'], level + 1))

def userValues():
    """ Функция, которая принимает данные от пользователя 
    Выходные данные: height, root, leftFunc, rightFunc или сообщение об ошибке """
    print("Генерация бинарного дерева")
    print("Введите параметры для дерева (нажмите Enter во любой строке для исп стандартных значений):")
    height = (input("Введите высоту дерева: "))
    root = (input("Введите значение корня дерева: "))
    leftFunc = input("Введите функцию для левой ветви (например, 'lambda x: x*2'): ")
    rightFunc = input("Введите функцию для правой ветви (например, 'lambda y: y+3'): ")
    # Проверка введенных значений
    if height != "" and root != "" and leftFunc != "" and rightFunc != "":
        if not callable(leftFunc) or not callable(rightFunc):
            return print("Функции должны быть callable")
        elif height < 1:
            return print("Высота дерева должна быть больше 0")
        elif height.isdigit() == False or root.isdigit() == False:
            return print("Значения height и root должны быть целочисленными")
        else:
            height = int(height)
            root = int(root)
            leftFunc = eval(leftFunc)
            rightFunc = eval(rightFunc)
            return print_tree(gen_bin_tree(height, root, (leftFunc), (rightFunc)))
    else:
        return print_tree(gen_bin_tree())

if __name__ == "__main__":
    userValues()