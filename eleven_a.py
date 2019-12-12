from intcode.intcomputer import IntComputer

def _coord_label(x, y):
    return "(%d, %d)" % (x, y)

DIRECTIONS = {
    "UP": 0,
    "RIGHT": 1,
    "DOWN": 2,
    "LEFT": 3
}

MOVEMENT_VECTORS = {
    "0": (0, 1),
    "1": (1, 0),
    "2": (0, -1),
    "3": (-1, 0)
}

class Panel:
    def __init__(self, x, y, colour=0):
        self.x = x
        self.y = y
        self.colour = colour

    def __str__(self):
        if self.colour == 1:
            return "#"

        if self.colour == 0:
            return " "

    def paint(self, new_colour):
        self.colour = new_colour

    def get_coords(self):
        return  _coord_label(self.x, self.y)


class Canvas:
    def __init__(self):
        self.panels = {}

    def get_panel(self, x, y):
        return self.panels.get(_coord_label(x, y)) or Panel(x, y)

    def paint_panel(self, x, y, colour):
        panel = self.get_panel(x, y)
        panel.paint(colour)
        self.panels[panel.get_coords()] = panel


class Robot:
    def __init__(self, program, canvas, x=0, y=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.orientation = DIRECTIONS["UP"]

        self.brain = IntComputer(program)
        self.brain.set_io_state([], False)

    def perform_turn(self, turn):
        self.orientation = (self.orientation + turn) % 4

    def turn_right(self):
        self.perform_turn(1)

    def turn_left(self):
        self.perform_turn(-1)

    def move_forwards(self):
        vector = MOVEMENT_VECTORS[str(self.orientation)]

        self.x = self.x + vector[0]
        self.y = self.y + vector[1]

    def run(self):
        while not self.brain.io_state.exited:
            # Feed in the current panel
            self.brain.append_input(self.canvas.get_panel(self.x, self.y).colour)

            # Run the brain
            self.brain.run_program()

            # Get and process outputs
            latest_outputs = self.brain.get_outputs()[-2:]
            paint_instruction = latest_outputs[0]
            turn_instruction = latest_outputs[1]

            # Paint first
            self.canvas.paint_panel(self.x, self.y, paint_instruction)

            # Then turn and move
            if turn_instruction == 0:
                self.turn_left()
            elif turn_instruction == 1:
                self.turn_right()

            self.move_forwards()


canvas = Canvas()

robot = Robot(
    [3,8,1005,8,327,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,28,1006,0,42,2,1104,11,10,1006,0,61,2,1005,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,65,1006,0,4,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,89,1,1108,10,10,1,1103,11,10,1,109,18,10,1006,0,82,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,126,2,109,7,10,1,104,3,10,1006,0,64,2,1109,20,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,163,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,185,2,1109,12,10,2,103,16,10,1,107,11,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,219,1,1005,19,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,245,2,1002,8,10,1,2,9,10,1006,0,27,1006,0,37,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,281,1006,0,21,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,306,101,1,9,9,1007,9,1075,10,1005,10,15,99,109,649,104,0,104,1,21102,1,847069852568,1,21101,344,0,0,1105,1,448,21101,0,386979963688,1,21101,355,0,0,1105,1,448,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,46346031251,1,1,21101,0,402,0,1105,1,448,21102,1,29195594775,1,21101,0,413,0,1105,1,448,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,868498428772,1,21101,0,436,0,1106,0,448,21102,718170641172,1,1,21102,1,447,0,1105,1,448,99,109,2,21202,-1,1,1,21102,40,1,2,21102,1,479,3,21102,1,469,0,1105,1,512,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,474,475,490,4,0,1001,474,1,474,108,4,474,10,1006,10,506,1101,0,0,474,109,-2,2106,0,0,0,109,4,2102,1,-1,511,1207,-3,0,10,1006,10,529,21101,0,0,-3,22101,0,-3,1,22101,0,-2,2,21101,0,1,3,21101,548,0,0,1106,0,553,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,576,2207,-4,-2,10,1006,10,576,21202,-4,1,-4,1106,0,644,22101,0,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,1,595,0,1105,1,553,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,614,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,636,22102,1,-1,1,21102,1,636,0,106,0,511,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0],
    canvas
)

robot.run()

print(str(len(canvas.panels)))
