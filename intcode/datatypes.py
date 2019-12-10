class Parameter:
    def __init__(self, input_mode, input_value):
        self.input_mode = input_mode
        self.input_value = input_value

    def resolve(self, program_state):
        if self.input_mode == 0:
            return program_state[self.input_value]

        if self.input_mode == 1:
            return self.input_value

class Output:
    def __init__(self, address):
        self.address = address

    def assign(self, value):
        return Mutation(self.address, value)


class Mutation:
    def __init__(self, program_address, new_value):
        self.program_address = program_address
        self.new_value = new_value

    def apply(self, program_state):
        new_prog_state = program_state[:]
        new_prog_state[self.program_address] = self.new_value

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

    def mark_exit(self):
        self.exited = True

