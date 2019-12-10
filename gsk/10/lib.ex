defmodule Input do
  def get(filename \\ "input.txt") do
    File.read!(filename)
    |> String.split("\n")
    |> Stream.with_index()
    |> Stream.flat_map(fn {row, y} ->
      String.codepoints(row)
      # we only care about indices with asteroids at them
      |> Stream.with_index()
      |> Stream.filter(fn {c, _} -> c == <<35>> end)
      |> Stream.map(fn {_, x} -> {x, y} end)
    end)
  end
end

defmodule Day10 do
  defp sq(x), do: :math.pow(x, 2)
  defp distance({xi, yi}, {x, y}), do: :math.sqrt(sq(xi - x) + sq(yi - y))

  defp visible(list, {x, y}) do
    Stream.filter(list, fn {xi, yi} -> xi != x || yi != y end)
    |> Enum.sort_by(fn i -> distance(i, {x, y}) end)
    |> Stream.map(fn {xi, yi} -> {xi, yi, :math.atan2(xi - x, yi - y)} end)
    |> Stream.uniq_by(fn {_, _, ang} -> ang end)
  end

  def optimal(list) do
    Enum.map(list, fn idx -> {idx, visible(list, idx) |> Enum.count()} end)
    |> Enum.max_by(fn {_, v} -> v end)
  end

  defp next_round(list, station_idx) do
    visible(list, station_idx)
    |> Enum.sort_by(fn {_, _, a} ->
      -a
    end)
    |> Enum.map(fn {x, y, _} -> {x, y} end)
  end

  def nth_vaporized(list, station_idx, n) do
    to_destroy = next_round(list, station_idx)
    num_destroyed = length(to_destroy)

    if num_destroyed > n - 1 do
      Enum.at(to_destroy, n - 1)
    else
      nth_vaporized(list -- to_destroy, station_idx, n - num_destroyed)
    end
  end
end
