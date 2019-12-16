#! /usr/bin/env elixir

Code.require_file("lib.ex")

rxns = Input.get("test.0.txt")

Constraints.index(rxns)
|> Constraints.dep("FUEL")
|> IO.inspect()
