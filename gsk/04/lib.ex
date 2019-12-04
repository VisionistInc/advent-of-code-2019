defmodule Password do
  defguardp six_digits?(password) when password > 99999 and password < 1_000_000

  defp monotonic?([]), do: true

  defp monotonic?([first, second | _]) when first > second, do: false

  defp monotonic?([_ | rest]) do
    monotonic?(rest)
  end

  defp has_doubles?([]), do: false

  defp has_doubles?([first, second | _]) when first == second, do: true

  defp has_doubles?([_ | rest]), do: has_doubles?(rest)

  defp has_strict_double?([a, b, c, d, e, f])
       when (a == b and b != c) or
              (a != b and b == c and c != d) or
              (b != c and c == d and d != e) or
              (c != d and d == e and e != f) or
              (d != e and e == f),
       do: true

  defp has_strict_double?(_), do: false

  def valid?(password) when six_digits?(password) do
    digits = Integer.digits(password)
    monotonic?(digits) && has_doubles?(digits)
  end

  def valid?(_), do: false

  def strictly_two?(password) do
    password |> Integer.digits() |> has_strict_double?
  end
end
