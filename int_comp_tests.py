from intcode.intcomputer import IntComputer

comp1 = IntComputer([3,9,8,9,10,9,4,9,99,-1,8])

comp1.add_test_case(None, [7], [0])
comp1.add_test_case(None, [8], [1])
comp1.add_test_case(None, [9], [0])

if comp1.run_tests():
    print("Tests passed!")

comp2 = IntComputer([3,3,1107,-1,8,3,4,3,99])
comp2.add_test_case(None, [7], [1])
comp2.add_test_case(None, [8], [0])

if comp2.run_tests():
    print("Tests passed!")
