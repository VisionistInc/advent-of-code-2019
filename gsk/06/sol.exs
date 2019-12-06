#! /usr/bin/elixir
Code.require_file("lib.ex")

universe =
  Input.get()
  |> Day6.graph()

IO.puts("Part 1: " <> to_string(Day6.count(universe)))
IO.puts("Part 2: " <> to_string(Day6.diff(universe, "YOU", "SAN")))
