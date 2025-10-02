import math

def sphere_volume(radius):
    return (4/3) * math.pi * (radius ** 3)

radius = 5
print(f"Volume of sphere with radius {radius}: {sphere_volume(radius):.2f}")