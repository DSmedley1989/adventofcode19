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

    def get_energy(self):
        return self.position.manhattan_magnitude() * self.velocity.manhattan_magnitude()

io = Moon("Io", Vector(4, 12, 13))
europa = Moon("Europa", Vector(-9, 14, -3))
ganymede = Moon("Ganymede", Vector(-7, -1, 2))
callisto = Moon("Callisto", Vector(-11, 17, -1))

SIM_LENGTH = 2584
PRINT_EVERY = 2584

moons = {
    io.name: io,
    europa.name: europa,
    ganymede.name: ganymede,
    callisto.name: callisto
}

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

def print_state(iteration):
    print("System State at t=%d" % iteration)
    print("\n".join([str(moon) for _, moon in moons.items()]))
    print("Total system energy = %d" % get_total_energy())

for step in range(0, SIM_LENGTH + 1):
    if step % PRINT_EVERY == 0:
        print_state(step)

    apply_gravity()
    apply_velocity()

