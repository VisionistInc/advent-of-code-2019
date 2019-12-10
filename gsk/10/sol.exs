#! /usr/bin/elixir

Code.require_file("lib.ex")

asteroids = Input.get()
{location, num_visible} = Day10.optimal(asteroids)

# part 1
IO.puts("Part 1: " <> to_string(num_visible))

# part 2
{x, y} = Day10.nth_vaporized(asteroids, location, 200)
IO.puts("Part 2: " <> to_string(100 * x + y))
