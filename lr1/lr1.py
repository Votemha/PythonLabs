# тестовые данные
nums1 = [2,7,11,15]
target1 = 9

nums2 = [3,2,4]
target2 = 6

nums3 = [3,3]
target3 = 6

# функция, в которой проходим в 2 цикла и сравниваем: сумму двух элементов и target
def two_sums(nums, target):

    for a in range(len(nums)):


        # проверка, что в массиве минимум 2 элемента
        if len(nums) >= 2:
            # проверка, что элемент - это целое число
            if isinstance(nums[a], int):
                    

                    for aSled in range(a+1, len(nums)):
                        if (nums[a] + nums[aSled]) == target:
                            return [a, aSled]
                        
            else: return "Один или несколько элементов не являются целыми числами"
        else: return "Недостаточно элементов в массиве"

    return "Нет решения"

         
# Example
print("Example 1:", two_sums(nums1, target1)) # ожидается: [0, 1]
print("Example 2:", two_sums(nums2, target2)) # ожидается: [1, 2]
print("Example 3:", two_sums(nums3, target3)) # ожидается: [0, 1]

# тест ожидаемых результатов внутри файла с функцией
# assert two_sums(nums, target) == [1,2], "Базовая проверка провалена"