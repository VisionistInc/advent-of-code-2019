defmodule Input do
  def get(file \\ "input.txt") do
    file |> File.read!() |> String.trim() |> String.codepoints() |> Enum.map(&String.to_integer/1)
  end
end

defmodule Day8 do
  def layers(pixels, {width, height}) do
    Enum.chunk_every(pixels, width * height)
  end

  def count_eq(e, value) do
    Enum.count(e, fn v -> v == value end)
  end

  defp merge({2, below}), do: below
  defp merge({this, _}), do: this

  def flatten([last]), do: last

  def flatten([this | rest]) do
    Enum.zip(this, flatten(rest)) |> Enum.map(&merge/1)
  end

  defp pixel(0), do: ' '
  defp pixel(1), do: '▩'

  def render(layer, width) do
    layer |> Enum.map(&pixel/1) |> Enum.chunk_every(width) |> Enum.join("\n")
  end
end
