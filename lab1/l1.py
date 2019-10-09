import math


def read_float_element(text):
    res = None
    while res is None:
        try:
            res = float(input(text))
        except ValueError:
            res = None
            print("Ошибка! Введите вещественное число.")
    return res


a = read_float_element("a: ")
b = read_float_element("b: ")
n = read_float_element("n: ")
x = read_float_element("x: ")

result = None

try:
    result = (5 * (math.pow(a, math.pow(n, x))) / math.log(a)) + math.sqrt(math.fabs(math.cos(math.pow(b, n)))) - \
             3 * math.pow(math.sin(a), 2)
except ZeroDivisionError:
    print("Деление на 0")
except OverflowError:
    print("Большие числа")

if result is not None:
    print("\nРезультат:", result)

