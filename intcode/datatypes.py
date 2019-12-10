class Parameter:
    def __init__(self, input_mode, input_value):
        self.input_mode = input_mode
        self.input_value = input_value

    def _get_address(self, program_state, address):
        if address + 1 > len(program_state):
            return 0
        else:
            return program_state[address]

    def resolve(self, program_state, io_state):
        if self.input_mode == 0:
            return self._get_address(program_state, self.input_value)

        if self.input_mode == 1:
            return self.input_value

        if self.input_mode == 2:
            return self._get_address(
                program_state,
                io_state.relative_base + self.input_value
            )

class Output:
    def __init__(self, output_mode, address):
        self.address = address
        self.output_mode = output_mode

    def assign(self, value):
        return Mutation(self.address, value, self.output_mode)


class Mutation:
    def __init__(self, program_address, new_value, output_mode):
        self.program_address = program_address
        self.new_value = new_value
        self.output_mode = output_mode

    def _expand_program_state(self, program_state, address):
        pos_relative_to_end = (address + 1) - len(program_state)
        new_prog_state = program_state[:]

        if pos_relative_to_end > 0:
            zeroes_to_pad = [0 for _ in range(0, pos_relative_to_end)]
            new_prog_state.extend(zeroes_to_pad)

        return new_prog_state

    def _handle_output_mode(self, io_state):
        if self.output_mode == 0:
            return self.program_address
        elif self.output_mode == 2:
            return io_state.relative_base + self.program_address
        else:
            raise Exception("Incompatible output mode!")


    def apply(self, program_state, io_state):
        address = self._handle_output_mode(io_state)
        new_prog_state = self._expand_program_state(program_state, address)
        new_prog_state[address] = self.new_value

        return new_prog_state

class TestCase:
    def __init__(self, test_program=None, test_input=[], expected_results=[]):
        self.input = test_input
        self.test_program = test_program
        self.expected_results = expected_results

    def get_program(self):
        return self.test_program

    def get_input(self):
        return self.input

    def test(self, output):
        return output == self.expected_result

class IOState:

    def __init__(self, inputs=None, output_to_shell=True):
        self.inputs = inputs
        self.output_to_shell = output_to_shell
        self.outputs = []
        self.exited = False
        self.awaiting_input = False
        self.relative_base = 0
    
    def is_halted(self):
        return self.exited or self.awaiting_input

    def get_input(self):
        if self.inputs is not None:
            if self.inputs:
                self.inputs.reverse()
                next_element = self.inputs.pop()
                self.inputs.reverse()
                return next_element
            else:
                self.awaiting_input = True
                return

        return int(input("Input required:"))

    def add_input(self, value):
        if self.inputs is not None:
            self.inputs.append(value)

        if self.awaiting_input:
            self.awaiting_input = False

    def output(self, value):
        self.outputs.append(value)

        if self.output_to_shell:
            print(str(value))

    def fetch_outputs(self):
        return self.outputs

    def adjust_relative_base(self, adjustment):
        self.relative_base = self.relative_base + adjustment

    def mark_exit(self):
        self.exited = True

