#! /usr/bin/env elixir

Code.require_file("../02/input.ex")
Code.require_file("lib.ex")

code = Input.get()

# part 1
blocks =
  %Machine{code: code}
  |> Game.last_frame()
  |> Enum.count(fn {_, _, v} -> v == 2 end)

IO.puts("Part 1: " <> to_string(blocks))

# part 2
score = Game.play(%Machine{code: put_elem(code, 0, 2)})

IO.puts("Part 2: " <> inspect(score))
