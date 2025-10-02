def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if (2 * chickens + 4 * rabbits) == numlegs:
            return chickens, rabbits
    return "No solution"

chickens, rabbits = solve(35, 94)
print(f"Chickens: {chickens}, Rabbits: {rabbits}")