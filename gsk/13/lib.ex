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

  def pixel(m) do
    case step(m) do
      nil ->
        nil

      {x, m} ->
        {y, m} = step(m)
        {id, m} = step(m)
        {m, {x, y, id}}
    end
  end

  def frame(m, buffer \\ []) do
    case pixel(m) do
      nil ->
        buffer

      {m, px} ->
        out = [px | buffer]

        if length(out) == 40 * 25 + 1 do
          {m, out}
        else
          frame(m, out)
        end
    end
  end
end

defmodule Game do
  def last_frame({m, _}), do: m |> Exec.frame() |> last_frame
  def last_frame(m) when is_map(m), do: m |> Exec.frame() |> last_frame
  def last_frame(pixels), do: pixels

  defp update_buffer([], px), do: [px]

  defp update_buffer([{xi, yi, _} | rest], {x, y, id})
       when x == xi and y == yi do
    [{x, y, id} | rest]
  end

  defp update_buffer([head | rest], px), do: [head | update_buffer(rest, px)]

  defp move([{x, y, p}, {xl, yl, nil} | rest]), do: move([{x, y, p}, {xl, yl, p} | rest])

  defp move([{bx, by, p}, {bx_l, by_l, p_l} | rest]) do
    vbx = bx - bx_l
    vby = by - by_l
    vp = p - p_l
    distance = bx - p

    same = distance == 0
    contact = same && by == 22
    tracking = vp == vbx
    right = vbx == 1
    left = vbx == -1
    up = vby < 0
    down = vby > 0

    synced = same && tracking

    l_r = length(rest)

    out =
      cond do
        l_r == 4427 -> [1]
        contact && right && (p < 20 || p > 22) && rem(p, 2) == 0 -> [1]
        contact && right -> [0, 1]
        contact && left -> [-1]
        p == 1 && up -> [1]
        p == 38 && (up || by < 21) -> [-1]
        l_r == 4715 || l_r == 4718 -> [-1]
        l_r == 4641 || l_r == 4716 -> [0, -1]
        l_r == 1780 || l_r == 2878 || l_r == 2907 -> [-1]
        synced && (l_r == 675 || l_r == 1032 || l_r == 1163) -> [-vp]
        right && down && distance >= 0 -> [1]
        right && distance > 0 -> [1]
        same && left && down && p == 1 -> [1]
        left && down && distance <= 0 -> [-1]
        left && distance < 0 -> [-1]
        vp == 0 -> [1]
        synced && p == 9 && l_r == 278 -> [vp]
        synced && p == 20 && l_r == 267 -> [-vp]
        synced && vp < 0 && p == 12 && l_r == 129 -> [-vp]
        synced && vp < 0 && l_r == 16 -> [1]
        synced && up && vp < 0 && (p == 5 || p == 7) && l_r < 200 -> [-vp]
        synced && up && (vp < 0 || p < 11) && l_r < 200 -> [vp]
        synced && up && l_r == 48 -> [-vp]
        synced && p == 11 && l_r == 60 -> [vp]
        synced && p == 11 && l_r == 78 -> [-vp]
        synced && p == 12 && l_r == 61 -> [-vp]
        synced && (by < 21 || l_r == 110) -> [vp]
        synced && l_r == 1324 -> [vp]
        same && !tracking -> [-vp]
        l_r == 1354 -> [vp]
        true -> [0, 0, vp]
      end

    # IO.puts(
    #   to_string(l_r) <>
    #     "\t" <>
    #     to_string(distance) <>
    #     "\t" <>
    #     to_string(p) <>
    #     " (" <>
    #     to_string(vp) <>
    #     ")\t" <>
    #     to_string(bx) <>
    #     " (" <>
    #     to_string(vbx) <>
    #     ")\t" <>
    #     to_string(by) <>
    #     " (" <>
    #     to_string(vby) <>
    #     ")\t" <>
    #     inspect(out)
    # )

    out
  end

  defp move(_), do: [-1]

  def play(m, score \\ 0, history \\ [], buffer \\ []) do
    case Exec.pixel(m) do
      {m, {-1, 0, score}} ->
        play(m, score, history, update_buffer(buffer, {-1, 0, score}))

      {m, {x, y, id}} when id == 3 or id == 4 ->
        next_frame = update_buffer(buffer, {x, y, id})

        {m, new_history} =
          case {id, history} do
            {3, [{bx, by, nil} | rest]} when bx != nil ->
              # next_frame |> render() |> IO.puts()
              hist = [{bx, by, x} | rest]
              {%Machine{m | inputs: move(hist)}, hist}

            {3, _} ->
              {m, [{nil, nil, x} | history]}

            {4, [{nil, nil, p} | rest]} when p != nil ->
              # next_frame |> render() |> IO.puts()
              hist = [{x, y, p} | rest]
              {%Machine{m | inputs: move(hist)}, hist}

            {4, _} ->
              {m, [{x, y, nil} | history]}
          end

        play(m, score, new_history, next_frame)

      {m, px} ->
        play(m, score, history, update_buffer(buffer, px))

      nil ->
        # buffer |> render() |> IO.puts()
        score
    end
  end

  def score([{-1, 0, s} | _]), do: s
  def score([]), do: 0
  def score([_ | rest]), do: score(rest)

  defp color(0), do: ' '
  defp color(1), do: '█'
  defp color(2), do: '░'
  defp color(3), do: '▀'
  defp color(4), do: '●'

  def render(pixels) do
    "\nSCORE: " <>
      (pixels |> score |> to_string) <>
      "\n" <>
      (pixels
       |> Enum.filter(fn {x, _, _} -> x >= 0 end)
       |> Enum.group_by(fn {_, y, _} -> y end)
       |> Enum.sort()
       |> Enum.map_join(
         "\n",
         fn {_, pxs} -> Enum.sort(pxs) |> Enum.map_join(fn {_, _, id} -> color(id) end) end
       ))
  end
end
