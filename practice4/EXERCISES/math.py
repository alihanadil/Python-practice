# 1 Write a Python program to convert degree to radian.
import math
# # deg = 15
# deg = int(input())
# print(f"{math.radians(deg):.6f}")

# 2 Write a Python program to calculate the area of a trapezoid.
# h, b1, b2 = list(map(int,input().split()))
# h = 5
# b1 = 5
# b2 = 6
# print((b1+b2)/2 * h)

# 3 Write a Python program to calculate the area of regular polygon.
n, l = list(map(int,input().split()))
area = (n * l ** 2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area:.0f}")
# 4 Write a Python program to calculate the area of a parallelogram.
n, m = list(map(int,input().split()))
print(n*m)