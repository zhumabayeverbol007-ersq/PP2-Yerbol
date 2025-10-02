def get_permutations(s):
    from itertools import permutations
    return [''.join(p) for p in permutations(s)]

word = "KBTU"
permutations = get_permutations(word)
print(f"Permutations of '{word}': {permutations}")