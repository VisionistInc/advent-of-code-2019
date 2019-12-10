#!/usr/bin/python3

import sys
import redis

r = redis.Redis()


class Computer:
    initdata = []
    with open("input.txt", "r") as infile:
        for line in infile.read().strip().split(","):
            initdata.append(int(line))

    def __init__(self, init_args, input_topic=None, output_topic=None):
        self.data = self.initdata.copy()
        self.args = list(init_args)
        self.args.reverse()
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.eip = 0

    # TODO implement support for 3 immediate operands (??? maybe ???)
    def _get_params(self):
        # two params
        immediate = f"{self.data[self.eip]:05d}"
        if immediate[2] == "1":
            eax = self.data[self.eip + 1]
        else:
            eax = self.data[self.data[self.eip + 1]]
        if self.data[self.eip] % 100 in [1, 2, 5, 6, 7, 8]:
            if immediate[1] == "1":
                ebx = self.data[self.eip + 2]
            else:
                ebx = self.data[self.data[self.eip + 2]]
            return eax, ebx
        return eax

    def computer(self):
        # instruction pointer
        output = ""

        while self.data[self.eip] != 99:
            # print(f"self.data[{self.eip}+] = {self.data[self.eip:self.eip+4]}")
            # add operands
            if self.data[self.eip] % 100 == 1:
                eax, ebx = self._get_params()

                self.data[self.data[self.eip + 3]] = eax + ebx
                self.eip += 4

            # multiply operands
            elif self.data[self.eip] % 100 == 2:
                eax, ebx = self._get_params()

                self.data[self.data[self.eip + 3]] = eax * ebx
                self.eip += 4

            # read from stdin (or cli args)
            elif self.data[self.eip] % 100 == 3:
                # if we have args left to consume, consume them.
                if len(self.args) > 0:
                    eax = int(self.args.pop())
                elif self.input_topic is not None:
                    eax = int(r.brpop(self.input_topic)[1])
                else:
                    valid_int = False
                    while not valid_int:
                        eax = input("> ")
                        try:
                            eax = int(eax)
                            valid_int = True
                        except ValueError:
                            print("Not a valid int!")
                            pass

                self.data[self.data[self.eip + 1]] = eax
                self.eip += 2

            # write to stdout
            elif self.data[self.eip] % 100 == 4:
                eax = self._get_params()
                if self.output_topic is not None:
                    r.lpush(self.output_topic, eax)
                else:
                    output += f"{eax}\n"

                self.eip += 2

            # jump if true
            elif self.data[self.eip] % 100 == 5:
                eax, ebx = self._get_params()

                if eax != 0:
                    self.eip = ebx
                else:
                    self.eip += 3

            # jump if false
            elif self.data[self.eip] % 100 == 6:
                eax, ebx = self._get_params()

                if eax == 0:
                    self.eip = ebx
                else:
                    self.eip += 3

            # less than
            elif self.data[self.eip] % 100 == 7:
                eax, ebx = self._get_params()

                if eax < ebx:
                    self.data[self.data[self.eip + 3]] = 1
                else:
                    self.data[self.data[self.eip + 3]] = 0

                self.eip += 4

            # equals
            elif self.data[self.eip] % 100 == 8:
                eax, ebx = self._get_params()

                if eax == ebx:
                    self.data[self.data[self.eip + 3]] = 1
                else:
                    self.data[self.data[self.eip + 3]] = 0

                self.eip += 4

            else:
                print(f"INVALID OPCODE {self.data[self.eip]}")
                sys.exit(1)


if __name__ == "__main__":
    com = Computer(init_args=sys.argv[1:])
    com.computer()
