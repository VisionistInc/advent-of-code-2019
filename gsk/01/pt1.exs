defmodule Day1 do
  defp fuel_eqn(mass) do
    div(mass, 3) - 2
  end

  def fuel_sum(["" | rest]) do
    fuel_sum(rest)
  end

  def fuel_sum([first | rest]) do
    fuel_eqn(String.to_integer(first)) + fuel_sum(rest)
  end

  def fuel_sum([]) do
    0
  end
end

input = File.read!("input.txt")
nums = String.split(input, "\n")

IO.puts(Day1.fuel_sum(nums))
