from unittest import TestCase
from prefix import Solution

class Test(TestCase):
    def test_odd(self):
        """Cases where the length of the list is odd"""
        nums = [1, 3, 4, 2, 2]
        self.assertEqual(Solution().middle(nums), 2)

    def test_even(self):
        """Cases where the length of the list is even"""
        nums = [1, 7, 3, 6, 5, 6]
        self.assertEqual(Solution().middle(nums), 3)
        
    def test_no_middle_even(self):
        """Cases where the length of the list is even and has no middle"""
        nums = [1, 7]
        self.assertEqual(Solution().middle(nums), -1)

    def test_no_middle_odd(self):
        """Cases where the length of the list is odd and has no middle"""
        nums = [1, 7, 2]
        self.assertEqual(Solution().middle(nums), -1)

    def test_none(self):
        """Cases where the length of the list is 0"""
        nums = []
        self.assertEqual(Solution().middle(nums), -1)

    def test_one(self):
        """Cases where the length of the list is 1"""
        nums = [2]
        self.assertEqual(Solution().middle(nums), 0)

    def test_index_zero(self):
        """Cases where the middle is at index 0"""
        nums = [2, 1, -1]
        self.assertEqual(Solution().middle(nums), 0)
        
    def test_index_last(self):
        """Cases where the middle is at the last index"""
        nums = [-1, 1, 2]
        self.assertEqual(Solution().middle(nums), 2)