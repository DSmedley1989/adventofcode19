from intcode.intcomputer import IntComputer

from twelve_a import Vector

TILE_IDS = {
    'unexplored': 0,
    'floor': 1,
    'wall': 2,
    'oxygen_system': 3,
    'robot': 99
}

TILE_SPRITES = {
    '0': '?',
    '1': ' ',
    '2': '■',
    '3': 'O',
    '99': 'R'
}

MOVEMENT_VECTORS = {
    '1': Vector(0, 1),
    '2': Vector(0, -1),
    '3': Vector(-1, 0),
    '4': Vector(1, 0)
}

class Tile:
    def __init__(self, position_vector, tile_id):
        self.position = Vector(x, y)
        self.id = tile_id

    def __str__(self):
        return TILE_SPRITES[str(self.id)]

    def get_coords(self):
        return str(self.position)


class Map:
    def __init__(self):
        self.tiles = {}

    def set_tile(self, tile):
        self.tiles[tile.get_coords()] = tile

    def get_tile(self, position_vector):
        return self.tiles.get(str(position_vector)) or Tile(position_vector, TILE_IDS['unexplored'])

    def lookup_adjacent(self, position_vector):
        return {
            str(direction): self.get_tile(position_vector.add(MOVEMENT_VECTORS[str(direction)])) for direction in range(1, 4)
        }

    def draw(self, robot_position=None):
        lowest_x = 0
        highest_x = 0
        lowest_y = 0
        highest_y = 0

        for _, tile in self.tiles.items():
            if tile.position.x < lowest_x:
                lowest_x = tile.position.x
            if tile.position.x > highest_x:
                highest_x = tile.position.x
            if tile.position.y < lowest_y:
                lowest_y = tile.position.y
            if tile.position.y > highest_y:
                highest_y = tile.position.y

        lowest_x -= 1
        lowest_y -= 1
        highest_x += 1
        highest_y += 1

        full_map = [
            [
                self.get_tile(pos_x, pos_y) for pos_x in range(lowest_x, highest_x)
            ] for pos_y in range(lowest_y, highest_y)
        ]

        if robot_position:
            full_map[robot_position.y][robot_position.x] = Tile(robot_position, TILE_IDS['robot'])

        return (
            "\n".join(
                ["".join([str(tile) for tile in row]) for row in full_map]
            )
        )
