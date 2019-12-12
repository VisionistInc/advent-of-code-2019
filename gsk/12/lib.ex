defmodule Input do
  def get(filename \\ "input.txt") do
    File.read!(filename)
  end
end

defmodule Parse do
  defguardp is_ident(c) when c == ?x or c == ?y or c == ?z
  defguardp is_digit(d) when d > 47 and d < 58
  defguardp is_ignored(c) when c == 44 or c == 32 or c == 10 or c == 60

  defp get_number(<<45, rest::binary>>, []) do
    {num, unparsed} = get_number(rest, [])
    {-num, unparsed}
  end

  defp get_number(<<c, rest::binary>>, leading_digits) when is_digit(c) do
    get_number(rest, [c - 48 | leading_digits])
  end

  defp get_number(rest, []), do: {nil, rest}

  defp get_number(rest, digits) do
    {digits |> Enum.reverse() |> Integer.undigits(), rest}
  end

  defp moon(str, out \\ {nil, nil, nil})
  defp moon("", out), do: out
  defp moon(<<62, rest::binary>>, out), do: {out, rest}
  defp moon(<<c, rest::binary>>, t) when is_ignored(c), do: moon(rest, t)

  defp moon(<<c, ?=, rest::binary>>, out) when is_ident(c) do
    {val, more} = get_number(rest, [])
    moon(more, put_elem(out, c - 120, val))
  end

  def all_moons(str, out \\ []) do
    case moon(str) do
      {this, rest} -> [this | all_moons(rest)]
      {nil, nil, nil} -> out
    end
  end
end

defmodule Pairs do
  def get(list)
  def get([]), do: []

  def get([head | tail]) do
    for(elem <- tail, do: {head, elem}) ++ get(tail)
  end
end

defmodule Moon do
  defstruct [:position, velocity: {0, 0, 0}]
end

defmodule Physics do
  defp linear_dimension({x, y, z}), do: abs(x) + abs(y) + abs(z)

  defp potential(%Moon{position: p}), do: linear_dimension(p)
  defp kinetic(%Moon{velocity: v}), do: linear_dimension(v)

  def energy(m), do: potential(m) * kinetic(m)

  defp update_vel({pa, va}, {pb, vb}) do
    if pa == pb do
      {va, vb}
    else
      if pa > pb do
        {va - 1, vb + 1}
      else
        {va + 1, vb - 1}
      end
    end
  end

  defp gravitate(
         %Moon{
           position: {pxa, pya, pza},
           velocity: {vxa, vya, vza}
         },
         %Moon{
           position: {pxb, pyb, pzb},
           velocity: {vxb, vyb, vzb}
         }
       ) do
    {new_vxa, new_vxb} = update_vel({pxa, vxa}, {pxb, vxb})
    {new_vya, new_vyb} = update_vel({pya, vya}, {pyb, vyb})
    {new_vza, new_vzb} = update_vel({pza, vza}, {pzb, vzb})

    {%Moon{position: {pxa, pya, pza}, velocity: {new_vxa, new_vya, new_vza}},
     %Moon{position: {pxb, pyb, pzb}, velocity: {new_vxb, new_vyb, new_vzb}}}
  end

  defp advance(%Moon{position: {px, py, pz}, velocity: {vx, vy, vz}}) do
    %Moon{position: {px + vx, py + vy, pz + vz}, velocity: {vx, vy, vz}}
  end

  def axis_zero([]), do: true
  def axis_zero([0 | rest]), do: axis_zero(rest)
  def axis_zero(_), do: false

  def step(moons_list) do
    0..(length(moons_list) - 1)
    |> Enum.to_list()
    |> Pairs.get()
    |> Enum.reduce(List.to_tuple(moons_list), fn {ia, ib}, moons ->
      moon_a = elem(moons, ia)
      moon_b = elem(moons, ib)

      {new_moon_a, new_moon_b} = gravitate(moon_a, moon_b)

      put_elem(put_elem(moons, ia, new_moon_a), ib, new_moon_b)
    end)
    |> Tuple.to_list()
    |> Enum.map(&advance/1)
  end
end

defmodule Lcm do
  defp gcd(a, 0), do: a
  defp gcd(a, b), do: gcd(b, rem(a, b))

  defp two(a, b) do
    div(a, gcd(a, b)) * b
  end

  def get([last]), do: last

  def get([head | rest]) do
    two(head, get(rest))
  end
end
