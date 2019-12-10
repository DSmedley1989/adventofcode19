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
    return len(
        set([
                asteroid.get_theta() for asteroid in relative_asteroids
                if asteroid.not_at_origin()
            ])
        )


max_unique_lines_of_sight = 0

asteroids = extract_asteroids(convert_to_2d_list(INPUT_MAP))

for asteroid in asteroids:
    relative_asteroids = translate_origin(asteroids, asteroid)

    unique_thetas = get_unique_thetas(relative_asteroids)

    if unique_thetas > max_unique_lines_of_sight:
        max_unique_lines_of_sight = unique_thetas

print(str(max_unique_lines_of_sight))
