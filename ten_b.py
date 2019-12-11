import math

INPUT_MAP = """
.###.###.###.#####.#
#####.##.###..###..#
.#...####.###.######
######.###.####.####
#####..###..########
#.##.###########.#.#
##.###.######..#.#.#
.#.##.###.#.####.###
##..#.#.##.#########
###.#######.###..##.
###.###.##.##..####.
.##.####.##########.
#######.##.###.#####
#####.##..####.#####
##.#.#####.##.#.#..#
###########.#######.
#.##..#####.#####..#
#####..#####.###.###
####.#.############.
####.#.#.##########.
"""

TEST_MAP = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, target):
        return Asteroid(self.x - target.x, self.y - target.y)

    def detranslate(self, target):
        return Asteroid(self.x + target.x, self.y + target.y)

    def get_theta(self):
        return math.atan2(self.x, self.y)

    def get_r(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def not_at_origin(self):
        return self.x != 0 or self.y != 0


def convert_to_2d_list(input_string):
    return [
        [char for char in row.strip()] for row in input_string.strip().split("\n")
    ]

def extract_asteroids(two_dim_list):
    asteroids = []

    for y, row in enumerate(two_dim_list):
        for x, cell in enumerate(row):
            if cell == "#":
                asteroids.append(
                    Asteroid(x, y)
                )

    return asteroids

def extract_targets_directly(two_dim_list):
    targets = []
    laser_base = None

    for y, row in enumerate(two_dim_list):
        for x, cell in enumerate(row):
            if cell == "#":
                targets.append(
                    Asteroid(x, y)
                )
            elif cell == "X":
                laser_base = Asteroid(x, y)
    return laser_base, [target.translate(laser_base) for target in targets]

def translate_origin(asteroids, target_asteroid):
    return [
        asteroid.translate(target_asteroid) for asteroid in asteroids
    ]

def get_unique_thetas(relative_asteroids):
    return set([
            asteroid.get_theta() for asteroid in relative_asteroids
            if asteroid.not_at_origin()
        ])

def get_radius(asteroid):
    return asteroid.get_r()

max_unique_lines_of_sight = 0
unique_lines_of_sight = []
laser_base = None
targets = []

string_field = INPUT_MAP

if "X" in string_field:
    laser_base, targets = extract_targets_directly(convert_to_2d_list(string_field))
    unique_lines_of_sight = list(get_unique_thetas(targets))
else:
    asteroids = extract_asteroids(convert_to_2d_list(string_field))

    for asteroid in asteroids:
        relative_asteroids = translate_origin(asteroids, asteroid)

        unique_thetas = get_unique_thetas(relative_asteroids)


        if len(unique_thetas) > max_unique_lines_of_sight:
            max_unique_lines_of_sight = len(unique_thetas)
            unique_lines_of_sight = list(unique_thetas)
            laser_base = asteroid
            targets = [asteroid for asteroid in relative_asteroids if asteroid.not_at_origin()]

# Sort our targets by radius so closest get destroyed first
targets.sort(key=get_radius)

# Our thetas are in fact increasing anticlockwise
unique_lines_of_sight.sort(reverse=True)

rotated_lines_of_sight = []

last_target_destroyed = None
targets_destroyed = 0

print("Laser Base at %d, %d" % (laser_base.x, laser_base.y))
print("%d targets visible" % len(unique_lines_of_sight))
print("Targets (in order of distance from base):")
print("\n".join(["(%d, %d) at theta %.6f" % (target.x, target.y, target.get_theta()) for target in targets]))

print("Logic test")
test_first_theta = unique_lines_of_sight[0]
all_targets_with_matching_theta = [target for target in targets if target.get_theta() == test_first_theta]
print("All targets along line of sight %.6f:" % test_first_theta)
print("\n".join(["(%d, %d)" % (target.x, target.y) for target in all_targets_with_matching_theta]))

while targets_destroyed < 200:
    los = unique_lines_of_sight.pop(0)
    re_add_los = True

    for i, target in enumerate(targets):
        if target.get_theta() == los:
            targets.pop(i)
            abs_target = target.detranslate(laser_base)
            last_target_destroyed = target
            targets_destroyed += 1
            if targets_destroyed in [1,2,3,10,20,50,100,199,200]:
                print("%dth Target destroyed at %d, %d" % (targets_destroyed, abs_target.x, abs_target.y))
            break
    else:
        re_add_los = False

    if re_add_los:
        unique_lines_of_sight.append(los)

absolute_target = last_target_destroyed.detranslate(laser_base)

print(str("%s, %s" % (absolute_target.x, absolute_target.y)))
print(str((absolute_target.x * 100) + absolute_target.y))

