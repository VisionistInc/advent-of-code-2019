Code.require_file("input.ex")
Code.require_file("exec.ex")

defmodule Day2 do
  defp format(noun, verb) do
    verb + 100 * noun
  end

  defp next_inputs(noun, verb) when verb == 99 do
    {noun + 1, 0}
  end

  defp next_inputs(noun, verb) do
    {noun, verb + 1}
  end

  def attempt(code, {noun, verb}) do
    modded_code = put_elem(put_elem(code, 1, noun), 2, verb)

    if Exec.run(modded_code) == 19_690_720 do
      IO.puts(format(noun, verb))
    else
      attempt(code, next_inputs(noun, verb))
    end
  end
end

original = Input.get()

Day2.attempt(original, {0, 0})
