defmodule Input do
  defguardp is_space(c) when c == 32
  defguardp is_digit(c) when c > 47 and c < 58
  defguardp is_letter(c) when c > 64 and c < 91

  defp get_number(s, digits \\ "")

  defp get_number(<<c, rest::binary>>, digits) when is_space(c) do
    get_number(rest, digits)
  end

  defp get_number(<<c, rest::binary>>, digits) when is_digit(c) do
    get_number(rest, <<digits::binary, c>>)
  end

  defp get_number(s, ""), do: {nil, s}

  defp get_number(s, digits) do
    {String.to_integer(digits), s}
  end

  defp get_ident(s, out \\ "")

  defp get_ident(<<c, rest::binary>>, digits) when is_space(c) do
    get_ident(rest, digits)
  end

  defp get_ident(<<c, rest::binary>>, out) when is_letter(c) do
    get_ident(rest, <<out::binary, c>>)
  end

  defp get_ident(s, out), do: {out, s}

  defp get_qty(s) do
    {num, rest} = get_number(s)
    {ident, rest} = get_ident(rest)
    {{num, ident}, rest}
  end

  defp parse(str, out \\ {[], nil})
  defp parse("", out), do: out
  defp parse(<<",", rest::binary>>, out), do: parse(rest, out)
  defp parse(<<"=>", rest::binary>>, {inputs, nil}), do: parse(rest, {inputs, []})

  defp parse(s, {inputs, nil}) do
    {qty, rest} = get_qty(s)
    parse(rest, {[qty | inputs], nil})
  end

  defp parse(s, {inputs, outputs}) do
    {qty, rest} = get_qty(s)
    parse(rest, {inputs, [qty | outputs]})
  end

  def get(filename \\ "input.txt") do
    filename
    |> File.read!()
    |> String.split("\n")
    |> Enum.filter(fn s -> s != "" end)
    |> Enum.map(&parse/1)
  end
end

defmodule Constraints do
  def index(reactions, out \\ %{})
  def index([], out), do: out

  def index([{inputs, [{qty, output}]} | rest], out) do
    if Map.has_key?(out, output) do
      raise ArgumentError
    end

    index(rest, Map.put(out, output, {qty, inputs}))
  end

  defp gcd(a, 0), do: a
  defp gcd(a, b), do: gcd(b, rem(a, b))

  defp lcm(a, b) do
    div(a, gcd(a, b)) * b
  end

  def dep(graph, entry \\ {1, "FUEL"})
  def dep(graph, {n, "ORE"}), do: [{n, "ORE"}]

  def dep(graph, {n, ident}) do
    {qty, deps} = Map.get(graph, ident)

    batches =
      div(n, qty) +
        case rem(n, qty) do
          0 -> 0
          _ -> 1
        end

    deps
    |> Enum.map(fn {q, id} ->
      {q * batches, id}
    end)
    |> Enum.group_by(fn {_, id} -> id end)
    |> Enum.map(fn {id, ary} ->
      {Enum.reduce(ary, 0, fn {n, _}, s -> s + n end), id}
    end)
    |> Enum.flat_map(fn sub ->
      IO.inspect sub
      dep(graph, sub)
    end)
  end
end
