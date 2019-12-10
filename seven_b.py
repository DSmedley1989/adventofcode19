from intcode.intcomputer import IntComputer
from itertools import permutations

MASTER_PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,38,63,80,105,118,199,280,361,442,99999,3,9,102,5,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,4,9,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1001,9,5,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,5,9,101,3,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1002,9,2,9,1001,9,4,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99]
TEST_1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
possible_permutations = list(permutations([5,6,7,8,9]))

result_signals = []

def build_computer():
    return IntComputer(MASTER_PROGRAM)

amp_1 = build_computer()
amp_2 = build_computer()
amp_3 = build_computer()
amp_4 = build_computer()
amp_5 = build_computer()

all_amps = [amp_1, amp_2, amp_3, amp_4, amp_5]

def all_amps_exited():
    return (
        amp_1.io_state.exited and
        amp_2.io_state.exited and
        amp_3.io_state.exited and
        amp_4.io_state.exited and
        amp_5.io_state.exited
    )

def run_for_permutation(permutation):
    for amp in all_amps:
        amp.reset()
        amp.set_io_state([], False)

    for amp, config_val in list(zip(all_amps, permutation)):
        amp.append_input(config_val)

    value_to_feedback = 0

    while not all_amps_exited():
        amp_1.append_input(value_to_feedback)
        amp_1.run_program()

        amp_2.append_input(amp_1.get_outputs()[-1])
        amp_2.run_program()

        amp_3.append_input(amp_2.get_outputs()[-1])
        amp_3.run_program()

        amp_4.append_input(amp_3.get_outputs()[-1])
        amp_4.run_program()

        amp_5.append_input(amp_4.get_outputs()[-1])
        amp_5.run_program()

        value_to_feedback = amp_5.get_outputs()[-1]

    return value_to_feedback

for perm in possible_permutations:
    result_signal = run_for_permutation(perm)

    result_signals.append(result_signal)

highest_signal = result_signals[0]

for signal in result_signals[1:]:
    if signal > highest_signal:
        highest_signal = signal

print(str(highest_signal))
