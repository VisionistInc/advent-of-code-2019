#! /usr/bin/elixir

Code.require_file("../02/input.ex")
Code.require_file("lib.ex")

mch = %Machine{code: Input.get()}

# Part 1
[pt1] = Exec.run(%Machine{mch | inputs: [1]})
IO.puts("Part 1: " <> to_string(pt1))

# Part 2
[pt2] = Exec.run(%Machine{mch | inputs: [2]})
IO.puts("Part 1: " <> to_string(pt2))
