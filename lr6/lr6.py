import timeit
import matplotlib.pyplot as plt

def buildTreeRecursive(height, root, leftBranch=lambda x: x*2, rightBranch=lambda y: y+3):
    """ Функция, которая генерирует бинарное дерево 
    На вход принимает height и root
    Возвращает бинарное дерево в виде словаря или сообщение об ошибке """
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
        f"left {leftLeaf}": buildTreeRecursive(height-1, leftLeaf) if height > 1 else None,
        f"right {rightLeaf}": buildTreeRecursive(height-1, rightLeaf) if height > 1 else None
    }


'''
Функция для генерации бинарного дерева нерекурсивным методом
На вход принимает: 
высоту дерева, значение корня, функции для генерации левого и правого потомка
На выходе возвращает дерево в виде вложенных словарей
'''
def buildTreeIterative(height=5, root=1, leftBranch=lambda x: x*2, rightBranch=lambda y: y+3):
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


def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        # несколько повторов для усреднения
        times = timeit.repeat(lambda: func(n, 1, lambda x: x*2, lambda y: y+3), number=number, repeat=repeat)
        total += min(times)  # берём минимальное время из серии
    return total / len(data)

def main():
    # фиксированный набор данных
    test_data = list(range(1, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
        res_recursive.append(benchmark(buildTreeRecursive, [n], number=1000, repeat=5))
        res_iterative.append(benchmark(buildTreeIterative, [n], number=1000, repeat=5))
    

    # Первый график: итеративный с кешированием
    # Второй график: рекурсивный с кешированием
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
