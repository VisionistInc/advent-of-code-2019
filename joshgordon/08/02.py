#!/usr/bin/python3


width = 25
height = 6

pixels = height * width

layers = []
fewest_0s_layer = -1
fewest_0s_count = pixels + 1000

with open("input.txt") as infile:
    tmp = infile.read(pixels)
    while len(tmp) == pixels:
        layers.append(list(tmp))
        tmp = infile.read(pixels)

image = ["2"] * pixels

for i in range(pixels):
    for layer in layers:
        # 2 is transparent, carry on:
        if layer[i] != "2":
            image[i] = layer[i]
            break

for i in range(height):
    for j in range(width):
        if image[i * width + j] == "1":
            print("\u2588", end="")
        else:
            print(" ", end="")
    print()
