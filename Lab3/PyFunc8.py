def spy_game(nums):
    code = [0, 0, 7]
    for num in nums:
        if num == code[0]:
            code.pop(0)
        if not code:  # All numbers found
            return True
    return False

print(f"spy_game([1,2,4,0,0,7,5]): {spy_game([1,2,4,0,0,7,5])}")  # True
print(f"spy_game([1,0,2,4,0,5,7]): {spy_game([1,0,2,4,0,5,7])}")  # True
print(f"spy_game([1,7,2,0,4,5,0]): {spy_game([1,7,2,0,4,5,0])}")  # False