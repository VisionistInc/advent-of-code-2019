defmodule Input do
  defp to_ints([h | t]) do
    [String.to_integer(String.trim(h)) | to_ints(t)]
  end

  defp to_ints([]) do
    []
  end

  def get do
    List.to_tuple(to_ints(String.split(File.read!("input.txt"), ",")))
  end
end
