from collections import deque
class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        # ToDo: Write Your Code Here.
        candidates = set()
        count = {char: s.count(char) for char in set(s)}

        lst = deque()
        for i in range(len(s)):
            if s[i] not in candidates:
                while lst and count[lst[-1]] > 0 and s[i] < lst[-1]:
                    candidates.remove(lst.pop())
                lst.append(s[i])
                candidates.add(s[i])
            
            count[s[i]] -= 1
        
        return ''.join(lst)
    
