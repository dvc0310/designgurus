class Solution:
    def findDifferenceArray(self, nums):
        n = len(nums)
        if n == 0:
            return []
        differenceArray = [0] * n
        total_sum = sum(nums)
        left_sum = 0
        for i, num in enumerate(nums):
            right_sum = total_sum - num - left_sum
            differenceArray[i] = abs(right_sum - left_sum)
            left_sum += num
        return differenceArray
