defmodule Exec do
  defp eval(1, a, b) do
    a + b
  end

  defp eval(2, a, b) do
    a * b
  end

  defp step(code, position) when elem(code, position) == 99 do
    elem(code, 0)
  end

  defp step(code, position) do
    op = elem(code, position)

    ptr0 = elem(code, position + 1)
    ptr1 = elem(code, position + 2)

    in0 = elem(code, ptr0)
    in1 = elem(code, ptr1)

    out = elem(code, position + 3)

    result = eval(op, in0, in1)
    new_code = put_elem(code, out, result)
    step(new_code, position + 4)
  end

  def run(code) do
    step(code, 0)
  end
end
