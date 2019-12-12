defmodule Machine do
  defstruct code: {}, base: 0, inputs: [], ptr: 0

  def mem_get(code, ptr) when ptr < tuple_size(code), do: elem(code, ptr)
  def mem_get(_, _), do: 0

  def mem_put(code, ptr, value) when ptr < tuple_size(code) do
    put_elem(code, ptr, value)
  end

  def mem_put(code, ptr, value), do: mem_put(Tuple.append(code, 0), ptr, value)

  def opcode(%Machine{code: code, ptr: ptr}), do: elem(code, ptr)

  defp slot_value(i, slot) do
    mask = :math.pow(10, slot + 2) |> round
    rem(div(i, mask), 10)
  end

  def arg(%Machine{base: base, code: code, ptr: ptr}, arg_index) do
    op = elem(code, ptr)
    actual_arg = elem(code, ptr + 1 + arg_index)

    case slot_value(op, arg_index) do
      0 ->
        mem_get(code, actual_arg)

      1 ->
        actual_arg

      2 ->
        mem_get(code, base + actual_arg)
    end
  end

  def write_arg(%Machine{base: base, code: code, ptr: ptr}, arg_index) do
    op = elem(code, ptr)
    actual_arg = elem(code, ptr + 1 + arg_index)

    case slot_value(op, arg_index) do
      0 -> actual_arg
      2 -> actual_arg + base
    end
  end
end

defmodule Exec do
  import Machine

  defp eval(op, a, b) when rem(op, 100) == 1, do: a + b
  defp eval(op, a, b) when rem(op, 100) == 2, do: a * b
  defp eval(op, a, b) when rem(op, 100) == 7 and a < b, do: 1
  defp eval(op, _, _) when rem(op, 100) == 7, do: 0
  defp eval(op, a, b) when rem(op, 100) == 8 and a == b, do: 1
  defp eval(op, _, _) when rem(op, 100) == 8, do: 0

  defp step(m) do
    case rem(opcode(m), 100) do
      99 ->
        nil

      3 ->
        [new_elem | inputs] = m.inputs

        step(%Machine{
          m
          | code: mem_put(m.code, write_arg(m, 0), new_elem),
            ptr: m.ptr + 2,
            inputs: inputs
        })

      4 ->
        {
          arg(m, 0),
          %Machine{m | ptr: m.ptr + 2}
        }

      5 ->
        step(%Machine{
          m
          | ptr:
              if arg(m, 0) == 0 do
                m.ptr + 3
              else
                arg(m, 1)
              end
        })

      6 ->
        step(%Machine{
          m
          | ptr:
              if arg(m, 0) == 0 do
                arg(m, 1)
              else
                m.ptr + 3
              end
        })

      9 ->
        step(%Machine{m | base: m.base + arg(m, 0), ptr: m.ptr + 2})

      op ->
        result = eval(op, arg(m, 0), arg(m, 1))

        step(%Machine{
          m
          | code: mem_put(m.code, write_arg(m, 2), result),
            ptr: m.ptr + 4
        })
    end
  end

  defp go(nil, _, v), do: v
  defp go({out, m}, d, [{x, y} | rest]), do: go(step(m), d, [{x, y, out} | rest])

  defp go({out, m}, d, [current | rest]) do
    new_direction = Navigate.turn(d, out)
    new_position = Navigate.move(current, new_direction)
    {next_color, before} = Navigate.visit(new_position, rest)

    new_state = %Machine{m | inputs: [next_color]}

    go(step(new_state), new_direction, [new_position, current | before])
  end

  def run(code, initial) do
    go(step(%Machine{code: code, inputs: [initial]}), :up, [{0, 0}])
  end
end

defmodule Navigate do
  def turn(:up, 0), do: :left
  def turn(:up, 1), do: :right
  def turn(:right, 0), do: :up
  def turn(:right, 1), do: :down
  def turn(:down, 0), do: :right
  def turn(:down, 1), do: :left
  def turn(:left, 0), do: :down
  def turn(:left, 1), do: :up

  def move({x, y, _}, :up), do: {x, y - 1}
  def move({x, y, _}, :down), do: {x, y + 1}
  def move({x, y, _}, :right), do: {x + 1, y}
  def move({x, y, _}, :left), do: {x - 1, y}

  def visit(_, []), do: {0, []}
  def visit({x, y}, [{xi, yi, c} | rest]) when xi == x and yi == y, do: {c, rest}

  def visit(coords, [this | rest]) do
    {result, filtered_rest} = visit(coords, rest)
    {result, [this | filtered_rest]}
  end
end

defmodule Print do
  def go(painted) do
    init = {-1_000_000, -1_000_000, 1_000_000, 1_000_000}

    {max_y, max_x, min_y, min_x} =
      Enum.reduce(painted, init, fn {x, y, _}, {top, right, bottom, left} ->
        {
          max(y, top),
          max(x, right),
          min(y, bottom),
          min(x, left)
        }
      end)

    for y <- min_y..max_y do
      for x <- min_x..max_x do
        case Enum.find(painted, fn {xi, yi, _} -> xi == x && yi == y end) do
          {_, _, 1} -> '#'
          _ -> ' '
        end
      end
    end
    |> Enum.join("\n")
  end
end
