#! /usr/bin/elixir

Code.require_file("../02/input.ex")
Code.require_file("lib.ex")

code = Input.get()

pt1 =
  0..4
  |> Enum.to_list()
  |> Permutation.get()
  |> Enum.map(fn phases -> Day7.chain(code, phases) end)
  |> Enum.max()

IO.puts("Part 1: " <> to_string(pt1))

pt2 =
  5..9
  |> Enum.to_list()
  |> Permutation.get()
  |> Enum.map(fn phases -> Day7.chain_feedback(code, phases) end)
  |> Enum.max()

IO.puts("Part 2: " <> to_string(pt2))
