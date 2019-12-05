LOWER_BOUND = 168630
UPPER_BOUND = 718098

TEST_NUMBERS = [112233, 123444, 111122]
TEST_RESULTS = [True, False, True]

def split_to_digits(number):
    return [int(char) for char in str(number)]

def has_at_least_one_digit_pair(digits):
    digit_counts = {}

    for digit in digits:
        current_count = digit_counts.get(str(digit)) or 0
        digit_counts[str(digit)] = current_count + 1

    for digit, count in digit_counts.items():
        if count == 2:
            return True

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

    return has_at_least_one_digit_pair(digits) and has_increasing_digits(digits)

if __name__ == "__main__":
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
