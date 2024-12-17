
class Solution:
    def middle(self, nums):
        total_sum = sum(nums)
        right_sum = total_sum
        left_sum = 0
        for i, num in enumerate(nums):
            right_sum = total_sum - left_sum - num
            if right_sum == left_sum:
                return i
            left_sum += num 
        
        return -1