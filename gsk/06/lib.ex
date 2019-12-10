defmodule Input do
  defp to_pair(str) do
    String.split(str, ")")
    |> List.to_tuple()
  end

  def get(filename \\ "input.txt") do
    File.read!(filename)
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&to_pair/1)
  end
end

defmodule Day6 do
  defp direct({center, outer}, orbits) do
    update_in(orbits[center], fn list ->
      if list == nil do
        [outer]
      else
        [outer | list]
      end
    end)
  end

  defp children(direct_orbits, universe, center) do
    put_in(
      universe[center],
      case direct_orbits[center] do
        nil ->
          :end

        child_nodes ->
          Enum.reduce(child_nodes, %{}, fn child, orbits ->
            children(direct_orbits, orbits, child)
          end)
      end
    )
  end

  def graph(stars) do
    children(Enum.reduce(stars, %{}, &direct/2), %{}, "COM")
  end

  defp get_count({_, :end}, d), do: d

  defp get_count({_, m}, d), do: d + count(m, d + 1)

  defp count(map, depth) do
    Enum.map(map, fn v -> get_count(v, depth) end)
    |> Enum.sum()
  end

  def count(universe) do
    count(universe, 0)
  end

  defp find_depth(universe, id, depth \\ 0)
  defp find_depth(nil, _, _), do: false
  defp find_depth(:end, _, _), do: false

  defp find_depth(universe, id, d) do
    Enum.find_value(universe, fn {key, value} ->
      if key == id do
        d + 1
      else
        find_depth(value, id, d + 1)
      end
    end)
  end

  defp common(universe, id0, id1) do
    Enum.find_value(universe, fn {_, sub_universe} ->
      if find_depth(sub_universe, id0) && find_depth(sub_universe, id1) do
        common(sub_universe, id0, id1)
      end
    end) || universe
  end

  def diff(universe, id0, id1) do
    cmmn = common(universe, id0, id1)
    find_depth(cmmn, id0) + find_depth(cmmn, id1) - 2
  end
end
