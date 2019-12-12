#!/usr/bin/python3

import sys
import redis
from collections import defaultdict

r = redis.Redis()


class Computer:
    initdata = []
    with open("input.txt", "r") as infile:
        for line in infile.read().strip().split(","):
            initdata.append(int(line))

    def __init__(self, init_args, input_topic=None, output_topic=None):
        self.data = defaultdict(lambda: 0)
        for i in range(len(self.initdata)):
            self.data[i] = self.initdata[i]
        self.args = list(init_args)
        self.args.reverse()
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.relative_base = 0
        self.eip = 0

    # TODO implement support for 3 immediate operands (??? maybe ???)
    def _get_params(self):

        # two params
        immediate = f"{self.data[self.eip]:05d}"
        if immediate[2] == "1":
            eax = self.eip + 1
        elif immediate[2] == "2":
            eax = self.relative_base + self.data[self.eip + 1]
        else:
            eax = self.data[self.eip + 1]

        # hardcoded list of commands that take two arguments.
        if self.data[self.eip] % 100 in [1, 2, 5, 6, 7, 8]:
            if immediate[1] == "1":
                ebx = self.eip + 2
            elif immediate[1] == "2":
                ebx = self.relative_base + self.data[self.eip + 2]
            else:
                ebx = self.data[self.eip + 2]

            # hardcoded list of commands that take three arguments.
            if self.data[self.eip] % 100 in [1, 2, 7, 8]:
                if immediate[0] == "1":
                    ecx = self.eip + 3
                elif immediate[0] == "2":
                    ecx = self.relative_base + self.data[self.eip + 3]
                else:
                    ecx = self.data[self.eip + 3]
                return eax, ebx, ecx
            return eax, ebx
        return eax

    opcodes = {
        1: "add",
        2: "multiply",
        3: "read",
        4: "write",
        5: "jump if not zero",
        6: "Jump if zero",
        7: "less than",
        8: "equals",
        9: "adjust base",
    }

    def computer(self):
        while self.data[self.eip] != 99:
            # print("++++++++")
            # print(
            #     f"self.data[{self.eip}+] = {self.data[self.eip]} {self.data[self.eip+1]} {self.data[self.eip+2]} {self.data[self.eip+3]}"
            # )
            # print(f"Opcode {self.opcodes[self.data[self.eip] % 100]}")
            # add operands
            if self.data[self.eip] % 100 == 1:
                eax, ebx, ecx = self._get_params()

                self.data[ecx] = self.data[eax] + self.data[ebx]
                self.eip += 4

            # multiply operands
            elif self.data[self.eip] % 100 == 2:
                eax, ebx, ecx = self._get_params()

                self.data[ecx] = self.data[eax] * self.data[ebx]
                self.eip += 4

            # read from stdin (or cli args, or redis)
            elif self.data[self.eip] % 100 == 3:
                # if we have args left to consume, consume them.
                ebx = self._get_params()
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

                self.data[ebx] = eax
                self.eip += 2

            # write to stdout
            elif self.data[self.eip] % 100 == 4:
                eax = self._get_params()
                if self.output_topic is not None:
                    r.lpush(self.output_topic, self.data[eax])
                else:
                    print(self.data[eax])

                self.eip += 2

            # jump if true
            elif self.data[self.eip] % 100 == 5:
                eax, ebx = self._get_params()

                if self.data[eax] != 0:
                    self.eip = self.data[ebx]
                else:
                    self.eip += 3

            # jump if false
            elif self.data[self.eip] % 100 == 6:
                eax, ebx = self._get_params()

                if self.data[eax] == 0:
                    self.eip = self.data[ebx]
                else:
                    self.eip += 3

            # less than
            elif self.data[self.eip] % 100 == 7:
                eax, ebx, ecx = self._get_params()

                if self.data[eax] < self.data[ebx]:
                    self.data[ecx] = 1
                else:
                    self.data[ecx] = 0

                self.eip += 4

            # equals
            elif self.data[self.eip] % 100 == 8:
                eax, ebx, ecx = self._get_params()

                if self.data[eax] == self.data[ebx]:
                    self.data[ecx] = 1
                else:
                    self.data[ecx] = 0

                self.eip += 4

            # adjust relative base
            elif self.data[self.eip] % 100 == 9:
                eax = self._get_params()

                self.relative_base += self.data[eax]
                self.eip += 2

            else:
                print(f"INVALID OPCODE {self.data[self.eip]}")
                sys.exit(1)

            # print(
            #     f"self.data[{self.data[self.eip + 3]}]: {self.data[self.data[self.eip + 3]]}"
            # )


if __name__ == "__main__":
    com = Computer(init_args=sys.argv[1:])
    com.computer()
