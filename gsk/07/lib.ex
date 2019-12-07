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

  defp step(code, position, _) when elem(code, position) == 99 do
    nil
  end

  defp step(code, position, [new_elem | inputs]) when elem(code, position) == 3 do
    out = elem(code, position + 1)
    new_code = put_elem(code, out, new_elem)
    step(new_code, position + 2, inputs)
  end

  defp step(code, position, _) when rem(elem(code, position), 100) == 4 do
    ptr = elem(code, position + 1)

    {
      if elem(code, position) > 100 do
        ptr
      else
        elem(code, ptr)
      end,
      code,
      position + 2
    }
  end

  defp step(code, position, inputs) when rem(elem(code, position), 100) == 5 do
    op = elem(code, position)
    arg0 = elem(code, position + 1)
    arg1 = elem(code, position + 2)

    cnd =
      if rem(op, 1000) > 100 do
        arg0
      else
        elem(code, arg0)
      end

    jmp =
      if rem(op, 10000) > 1000 do
        arg1
      else
        elem(code, arg1)
      end

    step(
      code,
      if cnd == 0 do
        position + 3
      else
        jmp
      end,
      inputs
    )
  end

  defp step(code, position, inputs) when rem(elem(code, position), 100) == 6 do
    op = elem(code, position)
    arg0 = elem(code, position + 1)
    arg1 = elem(code, position + 2)

    cnd =
      if rem(op, 1000) > 100 do
        arg0
      else
        elem(code, arg0)
      end

    jmp =
      if rem(op, 10000) > 1000 do
        arg1
      else
        elem(code, arg1)
      end

    step(
      code,
      if cnd == 0 do
        jmp
      else
        position + 3
      end,
      inputs
    )
  end

  defp step(code, position, inputs) do
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
    step(new_code, position + 4, inputs)
  end

  def run(code, inputs, ptr \\ 0) do
    step(code, ptr, inputs)
  end
end

defmodule Permutation do
  defp get([], _), do: [[]]
  defp get(_, 0), do: [[]]

  defp get(list, k) do
    for head <- list, tail <- get(list -- [head], k - 1), do: [head | tail]
  end

  def get(list), do: get(list, length(list))
end

defmodule Day7 do
  def chain(code, phases, input \\ 0)

  def chain(_, [], input), do: input

  def chain(code, [phase | rest], input) do
    {out, _, _} = Exec.run(code, [phase, input])
    chain(code, rest, out)
  end

  defp stateful_exec([], [], [], input) do
    {input, [], []}
  end

  defp stateful_exec([code | code_stack], [ptr | ptr_stack], [phase | phase_stack], input) do
    case Exec.run(code, [phase, input], ptr) do
      nil ->
        nil

      {out, mem, resume} ->
        {next_out, next_mem, next_resume} = stateful_exec(code_stack, ptr_stack, phase_stack, out)

        {next_out, [mem | next_mem], [resume | next_resume]}
    end
  end

  defp feedback_until_nil(codes, ptrs, phases, input \\ 0) do
    case stateful_exec(codes, ptrs, phases, input) do
      nil ->
        input

      {output, new_codes, new_ptrs} ->
        feedback_until_nil(new_codes, new_ptrs, phases, output)
    end
  end

  def chain_feedback(code, phases) do
    feedback_until_nil(
      [code] |> Stream.cycle() |> Enum.take(length(phases)),
      [0] |> Stream.cycle() |> Enum.take(length(phases)),
      phases
    )
  end
end
