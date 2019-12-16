#!/usr/bin/env elixir

Code.require_file("../02/input.ex")
Code.require_file("intcode.ex")
Code.require_file("lib.ex")

code = Input.get()

mch = %Machine{code: code}

Navigate.find(mch)
|> IO.inspect
