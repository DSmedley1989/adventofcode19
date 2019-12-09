from intcode.datatypes import Parameter, Output, Mutation, IOState, TestCase
from intcode.instructions import get_instruction


class IntComputer:

    def __init__(self, master_program):
        self.master_program = master_program
        self.internal_program_state = self.master_program[:]
        self.prog_pointer = 0
        self.io_state = IOState()
        self.test_cases = []

    def add_test_case(self, test_program=None, test_input=[], expected_outputs=[]):
        self.test_cases.append(
            TestCase(test_program, test_input, expected_outputs)
        )

    def set_io_state(self, inputs, output_to_shell):
        self.io_state = IOState(inputs, output_to_shell)

    def _commit_mutation(self, mutation):
        self.internal_program_state = mutation.apply(self.internal_program_state)

    def _process_instruction(self, instruction):
        new_pointer, mutations, new_io_state = instruction.process(self.internal_program_state, self.io_state)
        self.prog_pointer = new_pointer
        self.io_state = new_io_state

        for mutation in mutations:
            self._commit_mutation(mutation)

    def run_program(self):
        while not self.io_state.exited:
            instruction = get_instruction(self.prog_pointer, self.internal_program_state)
            self._process_instruction(instruction)

    def get_outputs(self):
        return self.io_state.fetch_outputs()

    def reset(self):
        self.internal_program_state = self.master_program[:]
        self.prog_pointer = 0
        self.io_state = IOState()

    def run_tests(self):
        all_tests_passed = True

        for test in self.test_cases:
            self.reset()
            if test.get_program() is not None:
                self.internal_program_state = test.get_program()

            self.set_io_state(test.get_input(), output_to_shell=False)
            self.run_program()
            test_result = self.get_outputs() == test.expected_results

            if not test_result:
                print("Test failed! %s != %s" % (self.get_outputs(), test.expected_results))

            all_tests_passed = all_tests_passed and test_result

        self.reset()
        return all_tests_passed



