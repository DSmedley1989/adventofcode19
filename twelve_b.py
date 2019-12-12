import math

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "<%d, %d, %d>" % (self.x, self.y, self.z)

    def add(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def _vector_component_diff_to_unit(self, comp1, comp2):
        if comp1 == comp2:
            return 0

        if comp1 > comp2:
            return -1

        if comp1 < comp2:
            return 1

    def get_unit_direction_vector(self, other):
        return Vector(
            self._vector_component_diff_to_unit(self.x, other.x),
            self._vector_component_diff_to_unit(self.y, other.y),
            self._vector_component_diff_to_unit(self.z, other.z)
        )

    def manhattan_magnitude(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def get_inverse(self):
        return Vector(-self.x, -self.y, -self.z)


class Moon:
    def __init__(self, name, position=Vector(), velocity=Vector()):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.gravity_components = []

    def __str__(self):
        return "%s @ %s -> %s" % (self.name, str(self.position), str(self.velocity))

    def add_gravity_component(self, gravity_vector):
        self.gravity_components.append(gravity_vector)

    def apply_gravity(self):
        for gravity_component in self.gravity_components:
            self.velocity = self.velocity.add(gravity_component)

        self.gravity_components = []

    def apply_velocity(self):
        self.position = self.position.add(self.velocity)

    def get_x_state(self):
        return (self.position.x, self.velocity.x)

    def get_y_state(self):
        return (self.position.y, self.velocity.y)

    def get_z_state(self):
        return (self.position.z, self.velocity.z)

    def get_energy(self):
        return self.position.manhattan_magnitude() * self.velocity.manhattan_magnitude()

io = Moon("Io", Vector(4, 12, 13))
europa = Moon("Europa", Vector(-9, 14, -3))
ganymede = Moon("Ganymede", Vector(-7, -1, 2))
callisto = Moon("Callisto", Vector(-11, 17, -1))

SIM_LENGTH = 1000
PRINT_EVERY = 100

moons = {
    io.name: io,
    europa.name: europa,
    ganymede.name: ganymede,
    callisto.name: callisto
}

def get_lcm(numbers):
    lcm = 1
    while len(numbers):
        number = numbers.pop()
        lcm = int((lcm * number) / math.gcd(lcm, number))

    return lcm

#  Try resolving the repeating periods in each axis as they are independent


pairings = [
    (io.name, europa.name),
    (io.name, ganymede.name),
    (io.name, callisto.name),
    (europa.name, ganymede.name),
    (europa.name, callisto.name),
    (ganymede.name, callisto.name)
]

def apply_gravity():
    for pairing in pairings:
        moon_a = moons[pairing[0]]
        moon_b = moons[pairing[1]]
        gravity_between = moon_a.position.get_unit_direction_vector(moon_b.position)
        moon_a.add_gravity_component(gravity_between)
        moon_b.add_gravity_component(gravity_between.get_inverse())
        moons[pairing[0]] = moon_a
        moons[pairing[1]] = moon_b

    for name, moon in moons.items():
        moon.apply_gravity()
        moons[name] = moon

def apply_velocity():
    for name, moon in moons.items():
        moon.apply_velocity()
        moons[name] = moon

def get_total_energy():
    return sum([moon.get_energy() for _, moon in moons.items()])

def get_states_by_axis():
    x_states = [
        moon.get_x_state() for _, moon in moons.items()
    ]

    y_states = [
        moon.get_y_state() for _, moon in moons.items()
    ]

    z_states = [
        moon.get_z_state() for _, moon in moons.items()
    ]

    return {
        'x': x_states,
        'y': y_states,
        'z': z_states
    }

axis_periods = {}

def all_periods_found():
    return (
        axis_periods.get('x') is not None and
        axis_periods.get('y') is not None and
        axis_periods.get('z') is not None
    )

initial_states = get_states_by_axis()
current_step = 0
axes_yet_to_resolve = ['x', 'y', 'z']

while not all_periods_found():
    current_step += 1

    apply_gravity()
    apply_velocity()

    current_states = get_states_by_axis()

    for axis in axes_yet_to_resolve:
        if current_states[axis] == initial_states[axis]:
            print("Initial state recurred for %s axis after %d steps" % (axis, current_step))
            axis_periods[axis] = current_step

            axes_yet_to_resolve.remove(axis)

periods_found = [period for _, period in axis_periods.items()]

period_lcm = get_lcm(periods_found)

print("LCM for periods is %d" % period_lcm)
