#! /usr/bin/elixir

Code.require_file("lib.ex")

{width, height} = {25, 6}

layers = Input.get() |> Day8.layers({width, height})

# part 1
min_zero_layer = Enum.min_by(layers, fn layer -> Day8.count_eq(layer, 0) end)
pt1 = Day8.count_eq(min_zero_layer, 1) * Day8.count_eq(min_zero_layer, 2)

IO.puts("Part 1: " <> to_string(pt1))

# part 2
IO.puts("Part 2:")

layers
|> Day8.flatten()
|> Day8.render(width)
|> IO.puts()
