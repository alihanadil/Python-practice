#!/usr/bin/env python3
"""
map_filter_reduce.py

Examples and explanations for Python's map(), filter(), and reduce() functions.
These functions are pillars of functional programming in Python.
"""

from functools import reduce  # reduce is in the functools module

# ==============================
# map() - Apply a function to every item in an iterable
# ==============================
print("=" * 50)
print("map()")
print("=" * 50)

# map(function, iterable, ...) returns an iterator that applies function to every item.

# Example 1: Square each number in a list
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print("Squared numbers:", list(squared))  # [1, 4, 9, 16, 25]

# Example 2: Using a named function
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

celsius_temps = [0, 20, 30, 40]
fahrenheit_temps = list(map(celsius_to_fahrenheit, celsius_temps))
print("Fahrenheit temps:", fahrenheit_temps)  # [32.0, 68.0, 86.0, 104.0]

# Example 3: map with multiple iterables (function must accept that many arguments)
nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
summed = list(map(lambda x, y: x + y, nums1, nums2))
print("Sum of pairs:", summed)  # [5, 7, 9]

# Note: map stops at the shortest iterable if lengths differ.

# ==============================
# filter() - Keep items that satisfy a condition
# ==============================
print("\n" + "=" * 50)
print("filter()")
print("=" * 50)

# filter(function, iterable) returns an iterator with items for which function returns True.
# The function should return a boolean.

# Example 1: Keep only even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)  # [2, 4, 6, 8, 10]

# Example 2: Filter out None values
items = [1, None, 2, None, 3, 0, 4]
non_none = list(filter(lambda x: x is not None, items))
print("Without None:", non_none)  # [1, 2, 3, 0, 4]

# Example 3: Using None as the function (filters out falsey values)
truthy_items = list(filter(None, items))  # None, 0 are falsey
print("Truthy items (None as function):", truthy_items)  # [1, 2, 3, 4]

# ==============================
# reduce() - Cumulative reduction of items to a single value
# ==============================
print("\n" + "=" * 50)
print("reduce()")
print("=" * 50)

# reduce(function, iterable[, initializer]) applies function cumulatively to items,
# reducing the sequence to a single value. The function must take two arguments.

# Example 1: Sum of all numbers
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
print("Sum of numbers:", total)  # 15

# With an initial value
total_with_init = reduce(lambda acc, x: acc + x, numbers, 10)
print("Sum with initial 10:", total_with_init)  # 25

# Example 2: Find the maximum number
max_num = reduce(lambda a, b: a if a > b else b, numbers)
print("Maximum number:", max_num)  # 5

# Example 3: Build a dictionary from a list of key-value pairs
pairs = [("a", 1), ("b", 2), ("c", 3)]
dict_from_pairs = reduce(lambda d, kv: {**d, kv[0]: kv[1]}, pairs, {})
print("Dictionary from pairs:", dict_from_pairs)  # {'a': 1, 'b': 2, 'c': 3}

# ==============================
# Combining map, filter, reduce
# ==============================
print("\n" + "=" * 50)
print("Combining map, filter, reduce")
print("=" * 50)

# Task: Given a list of numbers, filter out odd numbers, square the evens, and sum them.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Step by step:
evens = filter(lambda x: x % 2 == 0, numbers)          # [2, 4, 6, 8, 10]
squared_evens = map(lambda x: x ** 2, evens)           # [4, 16, 36, 64, 100]
sum_squared_evens = reduce(lambda acc, x: acc + x, squared_evens, 0)

print("Sum of squares of evens:", sum_squared_evens)   # 220

# You can chain them in a single expression (though readability may suffer):
result = reduce(lambda acc, x: acc + x,
                map(lambda x: x ** 2,
                    filter(lambda x: x % 2 == 0, numbers)),
                0)
print("Chained result:", result)                        # 220

# ==============================
# Alternative: List comprehensions
# ==============================
print("\n" + "=" * 50)
print("List comprehensions (often more Pythonic)")
print("=" * 50)

# Many uses of map/filter can be replaced with comprehensions.
# The combined example above could be written as:
comprehension_result = sum(x**2 for x in numbers if x % 2 == 0)
print("Using comprehension + sum:", comprehension_result)  # 220

# Map example:
squared_comp = [x**2 for x in numbers]
print("Squared via comprehension:", squared_comp)

# Filter example:
evens_comp = [x for x in numbers if x % 2 == 0]
print("Evens via comprehension:", evens_comp)

# Note: reduce has no direct comprehension equivalent (but many cases can use sum(), max(), etc.)