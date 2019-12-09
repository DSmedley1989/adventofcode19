from intcode.datatypes import Parameter, Output, Mutation

def _split_to_digits(number):
    return [int(char) for char in str(number)]

def _parse_instruction(instruction):
    digits = _split_to_digits(instruction)

    if len(digits) == 1:
        return digits[0], []

    command = int("".join([str(d) for d in digits[-2:]]))
    input_modes = digits[:-2]

    return command, input_modes


def _read_args(pointer, program_state, num_args):
    return program_state[(pointer + 1):(pointer + num_args + 1)]


def _reverse_and_pad_modes(num_args, modes):
    diff = num_args - len(modes)

    zeroes = [ 0 for _ in range(0, diff)]
    modes.reverse()
    modes.extend(zeroes)

    return modes

def _get_args(pointer, input_modes, program_state, num_inputs, num_outputs):
    args = _read_args(pointer, program_state, num_inputs + num_outputs)
    modes = _reverse_and_pad_modes(num_inputs + num_outputs, input_modes)
    args_with_mode = list(zip(modes, args))

    params = [Parameter(i[0], i[1]) for i in args_with_mode[0:num_inputs]]
    outputs = [Output(i[1]) for i in args_with_mode[-num_outputs:]]

    return params, outputs


def _new_pointer(pointer, num_args):
    return pointer + num_args + 1

class ExitInstruction:
    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.program_state = program_state

    def process(self, program_state, io_state):
        io_state.mark_exit()
        return self.pointer, [], io_state

class AdditionInstruction:
    input_args = 2
    output_args = 1

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        result = a + b

        mutations = [out.assign(result) for out in self.outputs]

        return self.new_pointer(), mutations, io_state


class MultiplicationInstruction:
    input_args = 2
    output_args = 1

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        result = a * b

        mutations = [out.assign(result) for out in self.outputs]

        return self.new_pointer(), mutations, io_state


class UserInputInstruction:
    input_args = 0
    output_args = 1

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = io_state.get_input()

        mutations = [out.assign(a) for out in self.outputs]

        return self.new_pointer(), mutations, io_state


class OutputInstruction:
    input_args = 1
    output_args = 0

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        io_state.output(self.params[0].resolve(program_state))

        return self.new_pointer(), [], io_state


class JumpIfTrueInstruction:
    input_args = 2
    output_args = 0

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        if a != 0:
            return b, [], io_state

        return self.new_pointer(), [], io_state


class JumpIfFalseInstruction:
    input_args = 2
    output_args = 0

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        if a == 0:
            return b, [], io_state

        return self.new_pointer(), [], io_state


class LessThanInstruction:
    input_args = 2
    output_args = 1

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        result = 1 if a < b else 0

        mutations = [out.assign(result) for out in self.outputs]

        return self.new_pointer(), mutations, io_state


class EqualsInstruction:
    input_args = 2
    output_args = 1

    def new_pointer(self):
        return _new_pointer(self.pointer, self.input_args + self.output_args)

    def __init__(self, pointer, program_state, input_modes):
        self.pointer = pointer
        self.params, self.outputs = _get_args(pointer, input_modes, program_state, self.input_args, self.output_args)

    def process(self, program_state, io_state):
        a = self.params[0].resolve(program_state)
        b = self.params[1].resolve(program_state)

        result = 1 if a == b else 0

        mutations = [out.assign(result) for out in self.outputs]

        return self.new_pointer(), mutations, io_state


def get_instruction(pointer, program_state):
    command, input_modes = _parse_instruction(program_state[pointer])

    if command == 99:
        return ExitInstruction(pointer, program_state, input_modes)

    if command == 1:
        return AdditionInstruction(pointer, program_state, input_modes)

    if command == 2:
        return MultiplicationInstruction(pointer, program_state, input_modes)

    if command == 3:
        return UserInputInstruction(pointer, program_state, input_modes)

    if command == 4:
        return OutputInstruction(pointer, program_state, input_modes)

    if command == 5:
        return JumpIfTrueInstruction(pointer, program_state, input_modes)

    if command == 6:
        return JumpIfFalseInstruction(pointer, program_state, input_modes)

    if command == 7:
        return LessThanInstruction(pointer, program_state, input_modes)

    if command == 8:
        return EqualsInstruction(pointer, program_state, input_modes)

