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

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, target):
        return Asteroid(self.x - target.x, self.y - target.y)

    def get_theta(self):
        return math.atan2(self.x, self.y)

    def get_r(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def not_at_origin(self):
        return self.x != 0 or self.y != 0


def convert_to_2d_list(input_string):
    return [
        [char for char in row.strip()] for row in input_string.split("\n")
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

asteroids = extract_asteroids(convert_to_2d_list(INPUT_MAP))

for asteroid in asteroids:
    relative_asteroids = translate_origin(asteroids, asteroid)

    unique_thetas = get_unique_thetas(relative_asteroids)

    if len(unique_thetas) > max_unique_lines_of_sight:
        max_unique_lines_of_sight = len(unique_thetas)
        unique_lines_of_sight = list(unique_thetas)
        laser_base = asteroid
        targets = [asteroid for asteroid in asteroids if asteroid.not_at_origin()]

targets.sort(key=get_radius)
print(len(targets))
unique_lines_of_sight.sort(reverse=True)

rotated_lines_of_sight = [los for los in unique_lines_of_sight]

last_target_destroyed = None
targets_destroyed = 0

print("%d, %d" % (laser_base.x, laser_base.y))
print(str(len(unique_lines_of_sight)))

for los in rotated_lines_of_sight:

    targets_with_matching_los = 0

    for i, target in enumerate(targets):
        if target.get_theta() == los:
            targets_with_matching_los += 1
            # targets.pop(i)
            # last_target_destroyed = target
            # targets_destroyed += 1
            # print(str(targets_destroyed))
            # break
        else:
            print("%d - %d" % (target.get_theta(), los))
    print(str(targets_with_matching_los))


print(str(last_target_destroyed.x * 100 + last_target_destroyed.y))

