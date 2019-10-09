import math


func = lambda a, b, n, x: (5*(math.pow(a, math.pow(n, x)))/math.log(a)) + \
                          math.sqrt(math.fabs(math.cos(math.pow(b, n)))) - 3*math.pow(math.sin(a), 2)
try:
    list_elements = list(map(float, input().split(' ')))
except ValueError:
    print("Ошибка!")
    exit(-1)

print(func(list_elements[0], list_elements[1], list_elements[2], list_elements[3]))

