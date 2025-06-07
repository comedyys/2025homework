# pylint: disable=missing-module-docstring
def max_subarray_sum(arr):
    max_sum = float('-inf')
    current_sum = 0

    for num in arr:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


print(max_subarray_sum([1, -2, 3, 5, -1]))
print(max_subarray_sum([1, -2, 3, -8, 5, 1]))
print(max_subarray_sum([1, -2, 3, -2, 5, 1]))
