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

  def step(m) do
    case rem(opcode(m), 100) do
      99 ->
        nil

      3 ->
        case m.inputs do
          [new_elem | inputs] ->
            step(%Machine{
              m
              | code: mem_put(m.code, write_arg(m, 0), new_elem),
                ptr: m.ptr + 2,
                inputs: inputs
            })

          _ ->
            IO.puts("Ran out of inputs at IP " <> to_string(m.ptr))
            nil
        end

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
end
