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

for i in range(len(layers)):
    count = layers[i].count("0")
    print(f"layer {i} has {count} 0's")
    if count < fewest_0s_count:
        print(
            f"layer {i} beats layer {fewest_0s_layer} with {count} 0's instead of {fewest_0s_count}"
        )
        fewest_0s_count = count
        fewest_0s_layer = i


print(layers[fewest_0s_layer].count("1") * layers[fewest_0s_layer].count("2"))
