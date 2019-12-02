Code.require_file("input.ex")
Code.require_file("exec.ex")

code = Input.get()
modified_code = put_elem(put_elem(code, 1, 12), 2, 2)

IO.puts(Exec.run(modified_code))
