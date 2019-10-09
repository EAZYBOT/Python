import math


elip = lambda a: math.pi * a[0] * a[1]
circle = lambda r: math.pi * math.pow(r, 2)
polygon = lambda a: (a[0] * math.pow(a[1], 2)) / (4 * math.tan(math.pi / a[0]))

input_list = [[elip, circle, circle, polygon, elip, polygon], [(2, 3), 4, 5, (2, 1), (10, 5), (3, 6), (6, 9)]]

result_list = list(map(lambda f, a: f(a), input_list[0], input_list[1]))

print(result_list)
