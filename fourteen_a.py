import math


def _parse_reaction_definition(reaction_string):
    split_reaction = reaction_string.split("=>")
    ingredients = split_reaction[0].strip()
    product = split_reaction[1].strip()

    product_name = product.split(" ")[1]
    product_quantity = int(product.split(" ")[0])

    reactants = {}

    for raw_reactant in ingredients.split(","):
        reactant_name = raw_reactant.strip().split(" ")[1]
        reactant_quantity = int(raw_reactant.strip().split(" ")[0])

        reactants[reactant_name] = reactant_quantity

    return product_name, product_quantity, reactants


class Reaction:
    def __init__(self, reaction_string):
        self.product, self.quantity_produced, self.reactants = _parse_reaction_definition(reaction_string)
        self.order = None

    def number_reactions_required(self, desired_product_quantity):
        return int(math.ceil(float(desired_product_quantity) / float(self.quantity_produced)))

    def set_reaction_order(self, order):
        self.order = order

    def get_reactants_for_quantity(self, desired_product_quantity):
        required_number_reactions = self.number_reactions_required(desired_product_quantity)

        return {
            name: quantity * required_number_reactions for name, quantity in self.reactants.items()
        }

RAW_REACTIONS_INPUT = """
9 RJLWC, 9 RJCH => 9 QWFH
1 XZVHQ, 9 SPQR, 2 WKGVW => 5 KPZB
12 HPRPM, 4 GTZCK => 7 DJNDX
7 JKRV, 3 FKTLR, 19 FDSBZ => 9 HPRPM
9 VTCRJ => 4 SPSW
2 FDSBZ, 1 FKTLR => 6 KBJF
9 SPSW => 9 QHVSJ
5 TFPNF, 11 MNMBX, 1 QCMJ, 13 TXPL, 1 DJNDX, 9 XZVHQ, 2 WKGVW, 2 VQPX => 8 GPKR
10 DWTC, 8 DSPJG => 4 QCMJ
100 ORE => 9 XZDP
3 DBRBD => 4 DKRX
37 JKRV, 5 FKTLR => 7 VXZN
3 HWDS, 2 ZRBN => 8 XZVHQ
15 QNXZV, 53 VXZN, 3 LJQH, 13 FKXVQ, 6 DZGN, 17 MNMBX, 16 GPKR, 8 HWJVK => 1 FUEL
8 GSLWP => 7 PWTFL
4 HVPWG => 9 JKRV
5 NVWGS, 1 QWFH, 9 CWZRS => 2 XPMV
6 ZRBN => 4 JZDB
36 BWXWC, 14 HKFD => 3 FMNK
3 FMNK, 2 SPSW, 16 WKGVW => 6 VQPX
1 DWTC => 9 VMHM
3 HPRPM, 1 DWTC => 5 TXPL
1 KBJF, 2 ZSKSW => 1 MNMBX
5 JZDB => 4 FDSBZ
2 FKXVQ => 9 ZTFZG
17 XZDP => 2 HKFD
7 VMHM => 3 FGQF
1 JKRV => 8 CWZRS
1 WKGVW, 2 SPSW => 6 VLQP
3 ZRBN => 3 ZSKSW
7 VXZN, 7 TGLHX => 5 NVWGS
10 VLQP, 18 FGQF => 4 DBRBD
8 VMHM => 8 SPQR
1 KPZB, 4 GQGB, 3 WKGVW => 1 FDSZX
2 VXZN => 8 VTCRJ
3 RJLWC => 2 GQGB
6 TXPL => 4 DSPJG
2 ZTFZG => 8 TJLW
1 MPSPS => 3 BWXWC
5 FMNK, 4 ZSKSW => 5 RWKWD
137 ORE => 3 MPSPS
1 VTCRJ, 8 QWFH => 2 GKVQK
8 RJLWC => 8 TFPNF
7 TJLW, 1 TFPNF, 16 VQPX, 4 DBRBD, 4 GTZCK, 5 XPMV, 1 FDSZX => 6 DZGN
1 HVPWG => 7 RJLWC
18 HVPWG, 9 BWXWC => 4 GSLWP
107 ORE => 8 RJCH
1 RJCH => 2 ZRBN
2 GSLWP, 18 RWKWD, 1 QWFH => 5 LJQH
3 VXZN, 1 FMNK => 4 TGLHX
3 HKFD, 6 FMNK => 3 FKTLR
3 MPSPS => 4 HVPWG
27 PWTFL, 15 ZTFZG, 6 QHVSJ, 14 DJNDX, 9 RWKWD, 2 MNMBX, 4 DKRX => 6 QNXZV
1 ZSKSW, 9 KBJF => 3 FKXVQ
2 FDSBZ => 4 DWTC
3 HPRPM => 5 HWDS
1 GKVQK, 1 PWTFL => 5 GTZCK
1 FGQF => 5 WKGVW
5 FDSBZ, 7 SPSW => 6 HWJVK
"""

REACTIONS_AVAILABLE = {}

for reaction_string in RAW_REACTIONS_INPUT.strip().split("\n"):
    reaction = Reaction(reaction_string.strip())

    REACTIONS_AVAILABLE[reaction.product] = reaction

def determine_reaction_order(reactants):
    if list(reactants) == ['ORE']:
        return 1

    return max(
        [determine_reaction_order(REACTIONS_AVAILABLE[reactant].reactants) for reactant in list(reactants)]
    ) + 1

for name, reaction in REACTIONS_AVAILABLE.items():
    reaction_order = determine_reaction_order(reaction.reactants)

    reaction.set_reaction_order(reaction_order)

def get_order(reaction):
    return reaction.order

REACTIONS_IN_ORDER = [reaction for _, reaction in REACTIONS_AVAILABLE.items()]
REACTIONS_IN_ORDER.sort(key=get_order, reverse=True)

required_reactants = REACTIONS_AVAILABLE['FUEL'].get_reactants_for_quantity(1)

while len(required_reactants) > 1:
    print(str(required_reactants))

    for reaction in REACTIONS_IN_ORDER:
        if reaction.product not in required_reactants:
            continue

        quantity = required_reactants[reaction.product]

        new_reactants = reaction.get_reactants_for_quantity(quantity)

        # Update the counts with the new required reactants
        for new_reactant, additional_quantity in new_reactants.items():
            current_quantity = required_reactants.get(new_reactant) or 0

            required_reactants[new_reactant] = current_quantity + additional_quantity

        del required_reactants[reaction.product]

# Should only be ore left
print(str(required_reactants['ORE']))
