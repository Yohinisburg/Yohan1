#Algorithm. 1-1
def sqr_n(n):
    s = 0
    for i in range(1, n + 1):
        s = s + i ** 2
    return s

print(sqr_n(10))



def find_least(a):
    n = len(a)
    min_num = a[0]
    for i in range(1, n):
        if a[i] < min_num:
            min_num = a[i]
    return min_num

m = [10, 51, 93 , 0 , 104]
print(find_least(m))
