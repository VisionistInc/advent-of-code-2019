#! /usr/bin/env elixir

Code.require_file("lib.ex")

moons =
  Input.get()
  |> Parse.all_moons()
  |> Enum.map(fn pos -> %Moon{position: pos} end)

# part 1
total =
  1..1000
  |> Enum.reduce(moons, fn _, list -> Physics.step(list) end)
  |> Enum.map(&Physics.energy/1)
  |> Enum.sum()

IO.puts("Part 1: " <> to_string(total))

# part 2
half_period =
  Stream.repeatedly(fn -> nil end)
  |> Enum.reduce_while({moons, 1, {nil, nil, nil}}, fn _, {last, count, out} ->
    current = Physics.step(last)

    out_ =
      0..2
      |> Enum.reduce(out, fn idx, o ->
        if elem(o, idx) == nil &&
             current |> Enum.map(fn %Moon{velocity: v} -> elem(v, idx) end) |> Physics.axis_zero() do
          put_elem(o, idx, count)
        else
          o
        end
      end)

    if elem(out_, 0) != nil && elem(out_, 1) != nil && elem(out_, 2) != nil do
      {:halt, out_}
    else
      {:cont, {current, count + 1, out_}}
    end
  end)
  |> Tuple.to_list()
  |> Lcm.get()

IO.puts("Part 2: " <> to_string(half_period * 2))
