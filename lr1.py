# начальные данные
nums = [3,2,4]
target = 6

i = 0

# проходим в 2 цикла и сравниваем сумму двух элементов и target
for a in range(len(nums)-1):
    if nums[a] < target:
        for asled in range(a+1, len(nums)):
            if nums[a] + nums[asled] == target:
                print([a, asled])
                break