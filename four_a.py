LOWER_BOUND = 168630
UPPER_BOUND = 718098

TEST_NUMBERS = [111111, 223450, 123789]
TEST_RESULTS = [True, False, False]

def split_to_digits(number):
    return [int(char) for char in str(number)]

def has_two_matching_digits(digits):
    last_digit_examined = digits[0]

    for digit in digits[1:]:
        if digit == last_digit_examined:
            return True

        last_digit_examined = digit

    return False

def has_increasing_digits(digits):
    last_digit_examined = digits[0]

    for digit in digits[1:]:
        if digit < last_digit_examined:
            return False
        last_digit_examined = digit

    return True

def test_number(number):
    digits = split_to_digits(number)

    return has_two_matching_digits(digits) and has_increasing_digits(digits)

for i in range(0, 3):
    if test_number(TEST_NUMBERS[i]) != TEST_RESULTS[i]:
        print("Test %d failed!" % TEST_NUMBERS[i])
        break
else:
    print("Tests passed!")

total_possible_numbers = 0

for number in range(LOWER_BOUND, UPPER_BOUND + 1):
    if test_number(number):
        total_possible_numbers += 1

print(total_possible_numbers)
