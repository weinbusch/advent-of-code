def solve(data):
    polymer = data.strip()

    product = react(polymer)

    monomers = set(polymer.lower())

    shortest = sorted(len(react(polymer, exclude=m)) for m in monomers)[0]

    return len(product), shortest


def reacts_with(a, b):
    return a.lower() == b.lower() and a != b


def react(polymer, exclude=None):
    educt = list(m for m in reversed(polymer) if m.lower() != exclude)
    product = list()

    while educt:
        a = educt.pop()
        if product and reacts_with(a, product[-1]):
            product.pop()
        else:
            product.append(a)

    return product
