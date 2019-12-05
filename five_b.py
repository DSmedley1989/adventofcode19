from four_b import split_to_digits

INTCODE_PROGRAM = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,46,47,225,2,122,130,224,101,-1998,224,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1102,61,51,225,102,32,92,224,101,-800,224,224,4,224,1002,223,8,223,1001,224,1,224,1,223,224,223,1101,61,64,225,1001,118,25,224,101,-106,224,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,1102,33,25,225,1102,73,67,224,101,-4891,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,14,81,225,1102,17,74,225,1102,52,67,225,1101,94,27,225,101,71,39,224,101,-132,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,14,38,224,101,-1786,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1,65,126,224,1001,224,-128,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1101,81,40,224,1001,224,-121,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,7,226,226,224,102,2,223,223,1005,224,539,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,107,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,599,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,614,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

def parse_instruction(instruction):
    digits = split_to_digits(instruction)

    if len(digits) == 1:
        return digits[0], []

    command = int("".join([str(d) for d in digits[-2:]]))
    input_modes = digits[:-2]

    return command, input_modes


def read_args(pointer, num_args):
    return INTCODE_PROGRAM[(pointer + 1):(pointer + num_args + 1)]


def obtain_value(param):
    input_mode, input_value = param[0], param[1]
    if input_mode == 0:
        return INTCODE_PROGRAM[input_value]

    if input_mode == 1:
        return input_value


def reverse_and_pad_modes(num_args, modes):
    diff = num_args - len(modes)

    zeroes = [ 0 for _ in range(0, diff)]
    modes.reverse()
    modes.extend(zeroes)

    return modes


def get_args(pointer, input_modes, num_inputs, num_outputs):
    args = read_args(pointer, num_inputs + num_outputs)
    modes = reverse_and_pad_modes(num_inputs + num_outputs, input_modes)

    args_with_mode = list(zip(modes, args))

    inputs = args_with_mode[0:num_inputs]

    outputs = args_with_mode[-num_outputs:]

    return inputs, outputs


class ExitInstruction:
    def __init__(self, pointer):
        pass

    def process(self):
        exit()


class AdditionInstruction:
    input_args = 2
    output_args = 1

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        result = a + b

        for out in self.outputs:
            INTCODE_PROGRAM[out[1]] = result

        return self.pointer + self.input_args + self.output_args + 1


class MultiplicationInstruction:
    input_args = 2
    output_args = 1

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        result = a * b

        for out in self.outputs:
            INTCODE_PROGRAM[out[1]] = result

        return self.pointer + self.input_args + self.output_args + 1

class UserInputInstruction:
    input_args = 0
    output_args = 1

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = int(input("Input required:"))

        for out in self.outputs:
            INTCODE_PROGRAM[out[1]] = a

        return self.pointer + self.input_args + self.output_args + 1


class OutputInstruction:
    input_args = 1
    output_args = 0

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        print(str(obtain_value(self.inputs[0])))

        return self.pointer + self.input_args + self.output_args + 1


class JumpIfTrueInstruction:
    input_args = 2
    output_args = 0

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        if a != 0:
            return b

        return self.pointer + self.input_args + self.output_args + 1


class JumpIfFalseInstruction:
    input_args = 2
    output_args = 0

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        if a == 0:
            return b

        return self.pointer + self.input_args + self.output_args + 1

class LessThanInstruction:
    input_args = 2
    output_args = 1

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        result = 1 if a < b else 0

        for out in self.outputs:
            INTCODE_PROGRAM[out[1]] = result

        return self.pointer + self.input_args + self.output_args + 1

class EqualsInstruction:
    input_args = 2
    output_args = 1

    def __init__(self, pointer, input_modes):
        self.pointer = pointer
        self.inputs, self.outputs = get_args(pointer, input_modes, self.input_args, self.output_args)

    def process(self):
        a = obtain_value(self.inputs[0])
        b = obtain_value(self.inputs[1])

        result = 1 if a == b else 0

        for out in self.outputs:
            INTCODE_PROGRAM[out[1]] = result

        return self.pointer + self.input_args + self.output_args + 1


master_pointer = 0

while True:
    command, input_modes = parse_instruction(INTCODE_PROGRAM[master_pointer])

    if command == 99:
        ExitInstruction(master_pointer).process()

    elif command == 1:
        master_pointer = AdditionInstruction(master_pointer, input_modes).process()

    elif command == 2:
        master_pointer = MultiplicationInstruction(master_pointer, input_modes).process()

    elif command == 3:
        master_pointer = UserInputInstruction(master_pointer, input_modes).process()

    elif command == 4:
        master_pointer = OutputInstruction(master_pointer, input_modes).process()

    elif command == 5:
        master_pointer = JumpIfTrueInstruction(master_pointer, input_modes).process()

    elif command == 6:
        master_pointer = JumpIfFalseInstruction(master_pointer, input_modes).process()

    elif command == 7:
        master_pointer = LessThanInstruction(master_pointer, input_modes).process()

    elif command == 8:
        master_pointer = EqualsInstruction(master_pointer, input_modes).process()

    else:
        print("Unknown code %d encountered" % command)
        break
