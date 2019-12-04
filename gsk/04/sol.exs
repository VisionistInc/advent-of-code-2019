Code.require_file("lib.ex")

# Part 1
input = 137_683..596_253

valid_passwords =
  input
  |> Enum.filter(&Password.valid?/1)

valid_passwords
|> Enum.count()
|> IO.inspect()

# Part 2
valid_passwords
|> Enum.filter(&Password.strictly_two?/1)
|> Enum.count()
|> IO.inspect()
