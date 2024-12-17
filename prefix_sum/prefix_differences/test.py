from unittest import TestCase
from prefix_differences import Solution

class Test(TestCase):
    def test_default(self):
        """Default case"""
        nums = [2, 5, 1, 6, 1]
        expected = [13, 6, 0, 7, 14]
        self.assertEqual(Solution().findDifferenceArray(nums), expected)

    def test_one(self):
        """Case with one number"""
        nums = [2]
        expected = [0]
        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        
    def test_none(self):
        """Case with zero numbers"""
        nums = []
        expected = []
        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        
    def test_ascending(self):
        """Case with ascending numbers"""
        nums = [1, 2, 3, 4, 5]
        expected = [14, 11, 6, 1, 10]
        self.assertEqual(Solution().findDifferenceArray(nums), expected)

    def test_descending(self):
        """Case with descending numbers"""
        nums = [5, 4, 3, 2, 1]
        expected = [10, 1, 6, 11, 14]
        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        
    def test_index_zero(self):
        """Cases where the middle is at index 0"""
        nums = [2, 1, -1]
        expected = [0, 3, 3]

        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        
    def test_same(self):
        """Cases where all numbers are the same"""
        nums = [3, 3, 3]
        expected = [6, 0, 6]

        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        
    def test_index_last(self):
        """Cases where the middle is at the last index"""
        nums = [-1, 1, 2]
        expected = [3,3,0]
        
        self.assertEqual(Solution().findDifferenceArray(nums), expected)
        