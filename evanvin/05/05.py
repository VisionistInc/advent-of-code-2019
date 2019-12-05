import json


def requestNumber():
    print("\n")
    while True:
        num = input("Please enter the ID of the system you wish to test: ")
        if num.isdigit():
            return int(num)
        else:
            print("You did not enter a valid number.\n")


def runProgram(opcode):
    oc = opcode[:]
    idx = 0
    dtCodes = []
    cnt = 0

    while idx < len(oc) and cnt < 20:
        # print('idx: {} is {}'.format(idx, oc[idx]))
        padded = str(oc[idx]).zfill(5)
        opcode = int(padded[3:])
        paramMode1 = int(padded[2])
        paramMode2 = int(padded[1])
        paramMode3 = int(padded[0])
        try:
            param1 = oc[idx+1] if paramMode1 == 1 else oc[oc[idx+1]]
            param2 = oc[idx + 2] if paramMode2 == 1 else oc[oc[idx+2]]
            param3 = oc[idx+3]
        except:
            pass
        # print("oc-", opcode)
        # print("pm1-", paramMode1)
        # print("pm2-", paramMode2)
        # print("pm3-", paramMode3)
        # print("p1-", param1)
        # print("p2-", param2)
        # print("p3-", param3)

        if opcode is 1:
            # addition
            oc[param3] = param1+param2
            idx += 4
        elif opcode is 2:
            # multiplication
            oc[param3] = param1*param2
            idx += 4
        elif opcode is 3:
            ID = requestNumber()
            oc[oc[idx+1]] = ID
            idx += 2
        elif opcode is 4:
            print('Diagnostic test starting at position {} completed with code: {}'.format(
                idx, param1))
            dtCodes.append(param1)
            idx += 2
        elif opcode is 5:
            if param1 != 0:
                idx = param2
            else:
                idx += 3
        elif opcode is 6:
            if param1 == 0:
                idx = param2
            else:
                idx += 3
        elif opcode is 7:
            if param1 < param2:
                oc[param3] = 1
            else:
                oc[param3] = 0
            idx += 4
        elif opcode is 8:
            if param1 == param2:
                oc[param3] = 1
            else:
                oc[param3] = 0
            idx += 4
        elif opcode is 99:
            break

    # Create answer by checking if there were only two
    # types of diagnostic tests in the dtCodes list (0, and last dt code)
    return {'last_diagnostic_code': dtCodes[-1] if len(dtCodes) > 0 else 'No diagnostic codes were logged', 'thunderbirds_are_go': 0 < len(set(dtCodes)) < 3}


def puzzle(opcode):
    print('Run finished')
    return runProgram(opcode)


if __name__ == "__main__":
    inputText = open('input.txt', 'r')
    for line in inputText.readlines():
        opcode = [int(x) for x in line.split(',')]
        answer = {"puzzle_1_answer": puzzle(
            opcode), "puzzle_2_answer": puzzle(opcode)}
        with open('answers.json', 'w') as out:
            json.dump(answer, out)
