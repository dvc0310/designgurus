from unittest import TestCase
from remove_dupe import Solution

class Test(TestCase):
    def test_bad_order(self):
        """Test removing previous letters"""
        self.assertEqual(Solution().removeDuplicateLetters('babac'), 'abc')

    def test_single_order(self):
        """Test removing letters only when a duplicate is encountered"""
        self.assertEqual(Solution().removeDuplicateLetters('zabccde'), 'zabcde')

    def test_no_add(self):
        """Test skipping letters already in the string"""
        self.assertEqual(Solution().removeDuplicateLetters('mnopmn'), 'mnop')
        
    def test_multiple_same_letters(self):
        """Test multiple of the same letters"""
        self.assertEqual(Solution().removeDuplicateLetters('mmmmmmmmm'), 'm')

    def test_five(self):
        """Test number five"""
        self.assertEqual(Solution().removeDuplicateLetters('zyxxabdqxx'), 'zyabdqx')