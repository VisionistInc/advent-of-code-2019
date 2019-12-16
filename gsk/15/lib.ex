defmodule Day15 do
  defp color(0), do: '█'
  defp color(1), do: ' '
  defp color(2), do: '●'

  def render(list) do
    inits = {1_000_000, 1_000_000, -1_000_000, -1_000_000}

    {xmin, ymin, xmax, ymax} =
      Enum.reduce(list, inits, fn {x, y, _}, {xmin, ymin, xmax, ymax} ->
        {
          min(xmin, x),
          min(ymin, y),
          max(xmax, x),
          max(ymax, y)
        }
      end)

    ymin..ymax
    |> Enum.map_join("\n", fn yval ->
      xmin..xmax
      |> Enum.map_join(fn xval ->
        case Enum.find_value(list, fn {x, y, v} ->
               if x == xval && y == yval do
                 v
               end
             end) do
          nil -> 0
          other -> other
        end
        |> color
      end)
    end)
  end
end

defmodule Navigate do
  defp move(:north), do: [1]
  defp move(:south), do: [2]
  defp move(:west), do: [3]
  defp move(:east), do: [4]

  defp record(direction, val, [{x, y, 0} | rest]) do
    [new_elem | _] = record(direction, val, )
  end

  defp record(:north, val, world) do
    [{x, y, _} | _] = world
    [{x, y - 1, val} | world]
  end

  defp record(:south, val, world) do
    [{x, y, _} | _] = world
    [{x, y + 1, val} | world]
  end

  defp record(:west, val, world) do
    [{x, y, _} | _] = world
    [{x - 1, y, val} | world]
  end

  defp record(:east, val, world) do
    [{x, y, _} | _] = world
    [{x + 1, y, val} | world]
  end

  defguardp hit_wall(pt) when elem(pt, 2) == 1
  defguardp went_north(p0, p1) when elem(p0, 0) == elem(p1, 0) and elem(p0, 1) < elem(p1, 1)
  defguardp went_south(p0, p1) when elem(p0, 0) == elem(p1, 0) and elem(p0, 1) > elem(p1, 1)
  defguardp went_west(p0, p1) when elem(p0, 1) == elem(p1, 1) and elem(p0, 0) < elem(p1, 0)
  defguardp went_east(p0, p1) when elem(p0, 1) == elem(p1, 1) and elem(p0, 0) > elem(p1, 0)

  def find(m, world \\ [{0, 0, 1}])

  def find(_, [{x, y, 2} | rest]), do: [{x, y, 2} | rest]

  def find(m, world) do
    direction =
      case world do
        [p, p_last | _] when went_north(p, p_last) and hit_wall(p) -> :east
        [p, p_last | _] when went_north(p, p_last) -> :north
        [p, p_last | _] when went_east(p, p_last) and hit_wall(p) -> :north
        [p, p_last | _] when went_east(p, p_last) -> :east
        [p, p_last | _] when went_south(p, p_last) and hit_wall(p) -> :west
        [p, p_last | _] when went_south(p, p_last) -> :south
        [p, p_last | _] when went_west(p, p_last) and hit_wall(p) -> :north
        [p, p_last | _] when went_west(p, p_last) -> :west
        _ -> :north
      end

    {out, m} = Exec.step(%Machine{m | inputs: move(direction)})

    find(m, record(direction, out, world) |> IO.inspect())
  end
end
