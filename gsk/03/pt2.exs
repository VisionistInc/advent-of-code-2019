Code.require_file("lib.ex")

[wire_0, wire_1] = Input.get()

[path_0, path_1] = [WirePath.trace(wire_0), WirePath.trace(wire_1)]

IO.puts(WirePath.first(WirePath.intersect(path_0, path_1)))
