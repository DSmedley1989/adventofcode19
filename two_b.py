base_program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,9,19,23,1,6,23,27,2,27,9,31,2,6,31,35,1,5,35,39,1,10,39,43,1,43,13,47,1,47,9,51,1,51,9,55,1,55,9,59,2,9,59,63,2,9,63,67,1,5,67,71,2,13,71,75,1,6,75,79,1,10,79,83,2,6,83,87,1,87,5,91,1,91,9,95,1,95,10,99,2,9,99,103,1,5,103,107,1,5,107,111,2,111,10,115,1,6,115,119,2,10,119,123,1,6,123,127,1,127,5,131,2,9,131,135,1,5,135,139,1,139,10,143,1,143,2,147,1,147,5,0,99,2,0,14,0]

desired_output = 19690720

def test_case(noun, verb):
    clean_program = base_program[:]
    clean_program[1] = noun
    clean_program[2] = verb

    def process_instruction(root_index):
        instruction = clean_program[root_index]

        if instruction == 99:
            return False

        input_1_index = clean_program[root_index + 1]
        input_2_index = clean_program[root_index + 2]
        output_index = clean_program[root_index + 3]

        input_1 = clean_program[input_1_index]
        input_2 = clean_program[input_2_index]

        if instruction == 1:
            clean_program[output_index] = input_1 + input_2
        elif instruction == 2:
            clean_program[output_index] = input_1 * input_2
        else:
            print("Unknown instruction %s" % instruction)
            return False

        return True

    initial_step = 0

    while process_instruction(initial_step):
        initial_step += 4

    if clean_program[0] == desired_output:
        print("%s, %s" % (noun, verb))
        print((100 * noun) + verb)
        return True
    else:
        return False

for noun in range(0, 99):
    for verb in range(0, 99):
        if test_case(noun, verb):
            sys.exit()
