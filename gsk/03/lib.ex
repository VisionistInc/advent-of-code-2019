defmodule Input do
  defp read(fname) do
    String.split(String.trim(File.read!(fname), "\n"))
  end

  defp path(str) do
    String.split(str, ",")
  end

  defp get_path([]) do
    []
  end

  defp get_path([h | t]) do
    [path(h) | get_path(t)]
  end

  def get(fname \\ "input.txt") do
    get_path(read(fname))
  end
end

defmodule WirePath do
  defguardp between?(v, a, b) when (v > a and v <= b) or (v <= a and v > b)

  defp step({x, y}, <<?R, rest::binary>>) do
    dist = String.to_integer(rest)
    {x + dist, y, dist}
  end

  defp step({x, y}, <<?L, rest::binary>>) do
    dist = String.to_integer(rest)
    {x - dist, y, dist}
  end

  defp step({x, y}, <<?U, rest::binary>>) do
    dist = String.to_integer(rest)
    {x, y + dist, dist}
  end

  defp step({x, y}, <<?D, rest::binary>>) do
    dist = String.to_integer(rest)
    {x, y - dist, dist}
  end

  defp rasterize(current, []) do
    [current]
  end

  defp rasterize({start_x, start_y, already_traveled}, [move | rest]) do
    {x, y, dist} = step({start_x, start_y}, move)
    [{start_x, start_y, already_traveled} | rasterize({x, y, already_traveled + dist}, rest)]
  end

  def trace(path) do
    rasterize({0, 0, 0}, path)
  end

  defp manhattan(x, y) do
    abs(x) + abs(y)
  end

  defp check_cross(_, _, list) when length(list) < 2 do
    []
  end

  defp check_cross({x0, y0, dist}, {x1, y1, d1}, [{xi0, yi0, di0}, {xi1, yi1, di1} | rest])
       when x0 == x1 and yi0 == yi1 and between?(x0, xi0, xi1) and between?(yi0, y0, y1) do
    [
      {manhattan(x0, yi0), dist + abs(y0 - yi0) + di0 + abs(xi0 - x0)}
      | check_cross({x0, y0, dist}, {x1, y1, d1}, [{xi1, yi1, di1} | rest])
    ]
  end

  defp check_cross({x0, y0, dist}, {x1, y1, d1}, [{xi0, yi0, di0}, {xi1, yi1, di1} | rest])
       when y0 == y1 and xi0 == xi1 and between?(y0, yi0, yi1) and between?(xi0, x0, x1) do
    [
      {manhattan(xi0, y0), dist + abs(x0 - xi0) + di0 + abs(yi0 - y0)}
      | check_cross({x0, y0, dist}, {x1, y1, d1}, [{xi1, yi1, di1} | rest])
    ]
  end

  defp check_cross(pt0, pt1, [_, pt | rest]) do
    check_cross(pt0, pt1, [pt | rest])
  end

  def intersect([pt0, pt1 | rest], other) do
    check_cross(pt0, pt1, other) ++ intersect([pt1 | rest], other)
  end

  def intersect(_, _) do
    []
  end

  def closest(list) do
    List.foldr(list, 1_000_000, fn {m, _}, acc -> min(m, acc) end)
  end

  def first(list) do
    List.foldr(list, 1_000_000, fn {_, d}, acc -> min(d, acc) end)
  end
end
