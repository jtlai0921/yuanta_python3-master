"""
給定一個整數數組nums和一個目標值target，
請你在該數組中找出和為目標值的那兩個整數，並返回他們的數組index。
你可以假設每種輸入只會對應一個答案。
但是，你不能重複利用這個數組中同樣的元素。
nums = [2, 7, 11, 15]
target = 9
得到 [0, 1]

nums = [2, 7, 11, 15]
target = 22
得到 [1, 3]

nums = [2, 7, 11, 15]
target = 21
得到 None
"""


def two_sum(nums, target):
    """
    :type nums: list[int]
    :type target: int
    :rtype: list[int]
    [2, 7, 11, 15], 9
    """
    for index, num1 in enumerate(nums):
        num2 = target - num1
        if num1 != num2 and nums.count(num2) > 0:
            return [nums.index(num1), nums.index(num2)]

    return None


nums = [2, 7, 11, 15]
target = 9

print(two_sum(nums, target))
