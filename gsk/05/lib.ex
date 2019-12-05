defmodule Exec do
  defp eval(op, a, b) when rem(op, 100) == 1 do
    a + b
  end

  defp eval(op, a, b) when rem(op, 100) == 2 do
    a * b
  end

  defp eval(op, a, b) when rem(op, 100) == 7 do
    if a < b, do: 1, else: 0
  end

  defp eval(op, a, b) when rem(op, 100) == 8 do
    if a == b, do: 1, else: 0
  end

  defp step(code, position) when elem(code, position) == 99 do
    elem(code, 0)
  end

  defp step(code, position) when elem(code, position) == 3 do
    new_elem = IO.gets("") |> String.trim() |> String.to_integer()

    out = elem(code, position + 1)
    new_code = put_elem(code, out, new_elem)
    step(new_code, position + 2)
  end

  defp step(code, position) when rem(elem(code, position), 100) == 4 do
    ptr = elem(code, position + 1)

    if elem(code, position) > 100 do
      ptr
    else
      elem(code, ptr)
    end
    |> IO.puts()

    step(code, position + 2)
  end

  defp step(code, position) when rem(elem(code, position), 100) == 5 do
    op = elem(code, position)
    arg0 = elem(code, position + 1)
    arg1 = elem(code, position + 2)

    cnd = if rem(op, 1000) > 100 do
      arg0
    else
      elem(code, arg0)
    end

    jmp = if rem(op, 10000) > 1000 do
      arg1
    else
      elem(code, arg1)
    end

    if cnd == 0 do
      step(code, position + 3)
    else
      step(code, jmp)
    end
  end

  defp step(code, position) when rem(elem(code, position), 100) == 6 do
    op = elem(code, position)
    arg0 = elem(code, position + 1)
    arg1 = elem(code, position + 2)

    cnd = if rem(op, 1000) > 100 do
      arg0
    else
      elem(code, arg0)
    end

    jmp = if rem(op, 10000) > 1000 do
      arg1
    else
      elem(code, arg1)
    end

    if cnd == 0 do
      step(code, jmp)
    else
      step(code, position + 3)
    end
  end

  defp step(code, position) do
    op = elem(code, position)

    ptr0 = elem(code, position + 1)
    ptr1 = elem(code, position + 2)

    in0 =
      if rem(op, 1000) > 100 do
        ptr0
      else
        elem(code, ptr0)
      end

    in1 =
      if rem(op, 10000) > 1000 do
        ptr1
      else
        elem(code, ptr1)
      end

    out = elem(code, position + 3)

    result = eval(op, in0, in1)
    new_code = put_elem(code, out, result)
    step(new_code, position + 4)
  end

  def run(code) do
    step(code, 0)
  end
end
