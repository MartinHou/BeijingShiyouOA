def solve(s):
    ret, stk = [], []
    for i in range(len(s)):
        if s[i] == '(':
            stk.append(i)
            ret.append(' ')
        elif s[i] == ')':
            if len(stk) == 0:   # unmatched )
                ret.append('?')
            else:   # matched
                stk.pop()
                ret.append(' ')
        else:
            ret.append(' ')
    for i in stk:   # unmatched (
        ret[i] = 'x'
    return ''.join(ret)


print('Please input the count of lines:')
n = int(input())
res = ''
print('Please input the lines:')
for _ in range(n):
    line = input()
    res += line + '\n' + solve(line) + '\n'
print(res)

"""
4
bge)))))))))
((IIII))))))
()()()()(uuu
))))UUUU((()

"""
