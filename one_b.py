import math

input = [
    109044,
    60212,
    64742,
    142138,
    136568,
    75419,
    53333,
    92829,
    101974,
    129727,
    146189,
    59012,
    128230,
    82014,
    95644,
    104718,
    56678,
    140456,
    109579,
    76097,
    120110,
    129504,
    64430,
    107567,
    125459,
    149627,
    55625,
    113110,
    65923,
    96290,
    104284,
    144037,
    95560,
    84681,
    89824,
    122408,
    126032,
    54599,
    104811,
    127899,
    100164,
    69858,
    74350,
    111938,
    73606,
    144204,
    61446,
    87402,
    89622,
    113447,
    100960,
    134911,
    66807,
    75058,
    97648,
    131844,
    71501,
    52357,
    62832,
    140644,
    110284,
    132475,
    94625,
    146008,
    130087,
    124206,
    68642,
    52188,
    139127,
    83640,
    60401,
    102333,
    78650,
    138770,
    73078,
    60696,
    58898,
    87419,
    71292,
    69120,
    81081,
    50448,
    94644,
    103919,
    66507,
    90795,
    135753,
    84528,
    103454,
    91278,
    53749,
    126764,
    58397,
    54734,
    63086,
    60787,
    120579,
    110097,
    91947,
    105584
]

def calculate_fuel(mass):
    return math.floor(mass / 3.0) - 2

def calculate_total_fuel(payload_mass):
    total_fuel_required = 0
    additional_fuel = calculate_fuel(payload_mass)

    while additional_fuel > 0:
        total_fuel_required += additional_fuel
        additional_fuel = calculate_fuel(additional_fuel)

    return total_fuel_required


total_fuel = 0

for mass in input:
    total_fuel += calculate_total_fuel(mass)

print(total_fuel)