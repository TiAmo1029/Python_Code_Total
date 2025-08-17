from typing import List

class Solution:
    def brackets(self, s: str) -> bool:

        stack = []
        mapping = {
            ")": "(",
            "]": "[",
            "}": "{"
        }

        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'

                if mapping[char] != top_element:
                    return False

            else:
                stack.append(char)

        return not stack

solver = Solution()
s1 = "()["
s2 = "(){}{][]"
s3 = "{[]}"
s4 = "((()))"
s5 = "][{"

print(f"'{s1}', {solver.brackets(s1)}")
print(f"'{s2}', {solver.brackets(s2)}")
print(f"'{s3}', {solver.brackets(s3)}")
print(f"'{s4}', {solver.brackets(s4)}")
print(f"'{s5}', {solver.brackets(s5)}")