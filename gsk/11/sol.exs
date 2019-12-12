#! /usr/bin/env elixir

Code.require_file("../02/input.ex")
Code.require_file("lib.ex")

# part 1
painted =
  Input.get()
  |> Exec.run(0)
  |> tl

IO.puts("Part 1: " <> to_string(length(painted) + 1))

Print.go(painted) |> IO.puts()

# part 2

Input.get() |> Exec.run(1) |> tl |> Print.go() |> IO.puts()
