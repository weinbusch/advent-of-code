from math import log


def solve(data):
    decimal = sum(map(decode, data.splitlines()))
    return encode(decimal), None


example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""


def encode(decimal):
    n = decimal
    digits = []
    for exponent in range(int(log(n, 5)), -1, -1):
        mantissa, n = divmod(n, 5**exponent)
        digits.append(mantissa)
    shifted = []
    dx = 0
    for digit in reversed(digits):
        d = digit + dx
        dx, d = divmod(d, 5)
        d = (d + 2) % 5 - 2
        dx += 1 if d < 0 else 0
        shifted.append(d)
    if dx:
        shifted.append(dx)
    return "".join(map(encode_digit, reversed(shifted)))


def decode(snafu):
    chars = iter(reversed(snafu))
    digits = enumerate(map(decode_char, chars))
    decimal = sum(mantissa * 5**exponent for exponent, mantissa in digits)
    return decimal


def encode_digit(digit):
    lookup_table = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }
    return lookup_table[digit]


def decode_char(char):
    lookup_table = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    return lookup_table[char]


assert sum(map(decode, example.splitlines())) == 4890
assert encode(4890) == "2=-1=0", f"encode error: {encode(4890)} is not equal to 2=-1=0"

brochure = """  Decimal          SNAFU
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
"""

for line in brochure.splitlines():
    x, y = line.split()
    if not x.isdigit():
        continue
    x = int(x)
    assert encode(x) == y, f"error when encoding {x}: {encode(x)} is not equal to {y}"
    assert decode(y) == x, f"decode error: {decode(y)} is not equal to {x}"
