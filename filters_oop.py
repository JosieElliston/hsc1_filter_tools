from __future__ import annotations
import dataclasses
import functools
import itertools
from typing import Iterable, Sequence
import sys


@dataclasses.dataclass(frozen=True)
class Filter:
    s: str

    def to_int(self) -> int:
        return int(self.s, base=16)

    @staticmethod
    def _from_int(n: int) -> str:
        return hex(n)[2:].zfill(20)

    @staticmethod
    def from_int(n: int) -> Filter:
        return Filter(Filter._from_int(n))

    def __post_init__(self):
        assert self.s == Filter._from_int(self.to_int())

    def __inv__(self) -> Filter:
        return Filter.from_int(~self.to_int())

    def __and__(self, other: Filter) -> Filter:
        return Filter.from_int(self.to_int() & other.to_int())

    def __or__(self, other: Filter) -> Filter:
        return Filter.from_int(self.to_int() | other.to_int())

    # def __add__(self, other: Filter) -> Filter:
    #     return Filter.from_int(self.to_int() | other.to_int())

    def __sub__(self, other: Filter) -> Filter:
        return Filter.from_int(self.to_int() & ~other.to_int())

    @staticmethod
    def union(filters: Iterable[Filter]) -> Filter:
        it = iter(filters)
        first = next(it)
        return functools.reduce(lambda a, b: a | b, it, first)

    @staticmethod
    def intersection(filters: Iterable[Filter]) -> Filter:
        it = iter(filters)
        first = next(it)
        return functools.reduce(lambda a, b: a & b, it, first)


def write_sequence(f, seq: Iterable[tuple[str, Filter]]) -> None:
    # ---
    # - preset_name: cross
    #   visible_pieces: 000204080a5ab0004080
    f.write("---\n")
    for name, filter in seq:
        f.write(f"- preset_name: {name}\n")
        f.write(f'  visible_pieces: "{filter.s}"\n')


def print_sequence(seq: Iterable[tuple[str, Filter]]) -> None:
    write_sequence(sys.stdout, seq)


NOTHING = Filter("00000000000000000000")
EVERYTHING = Filter("ffffffffffffffffffff")

# pieces that are on each cell
# so each filter contains 27 pieces
cells = {
    "R": Filter("42942942949429429429"),
    "L": Filter("94294294292942942942"),
    "U": Filter("0000cf70000ff10008ff"),
    "D": Filter("ff10008ff0000ef30000"),
    "F": Filter("70e0c18307070e0c1830"),
    "B": Filter("0c183070e0e0c183070e"),
    "I": Filter("ffffff70000000000000"),
    "O": Filter("0000000000000effffff"),
}


# piece type filters

centers = {c: cells[c] - Filter.union(set(cells.values()) - {cells[c]}) for c in cells}

ridges = {
    (c1 + c2): (cells[c1] & cells[c2])
    - Filter.union(set(cells.values()) - {cells[c1], cells[c2]})
    for c1, c2 in itertools.combinations(cells.keys(), 2)
}
ridges = {k: v for k, v in ridges.items() if v != NOTHING}

edges = {
    (c1 + c2 + c3): (cells[c1] & cells[c2] & cells[c3])
    - Filter.union(set(cells.values()) - {cells[c1], cells[c2], cells[c3]})
    for c1, c2, c3 in itertools.combinations(cells.keys(), 3)
}
edges = {k: v for k, v in edges.items() if v != NOTHING}

corners = {
    (c1 + c2 + c3 + c4): (cells[c1] & cells[c2] & cells[c3] & cells[c4])
    - Filter.union(set(cells.values()) - {cells[c1], cells[c2], cells[c3], cells[c4]})
    for c1, c2, c3, c4 in itertools.combinations(cells.keys(), 4)
}
corners = {k: v for k, v in corners.items() if v != NOTHING}


# f2l filters

TOP = "I"
BASE = next(c for c in cells if cells[c] & cells[TOP] == NOTHING)

pairs_a = {
    (c1 + c2): (cells[c1] & cells[c2])
    - Filter.union(set(cells.values()) - {cells[c1], cells[c2], cells[BASE]})
    for c1, c2 in itertools.combinations(cells.keys(), 2)
    if len({c1, c2} & {TOP, BASE}) == 0
}
pairs_a = {k: v for k, v in pairs_a.items() if v != NOTHING}

pairs_b = {
    (c1 + c2 + c3): (cells[c1] & cells[c2] & cells[c3])
    - Filter.union(set(cells.values()) - {cells[c1], cells[c2], cells[c3], cells[BASE]})
    for c1, c2, c3 in itertools.combinations(cells.keys(), 3)
    if len({c1, c2, c3} & {TOP, BASE}) == 0
}
pairs_b = {k: v for k, v in pairs_b.items() if v != NOTHING}


def cfop_f2l_a_1() -> list[tuple[str, Filter]]:
    cross = Filter.union(ridges.values()) & cells[BASE]
    # RU + LU
    # RD + LD
    # UF + UB
    # DF + DB
    return [
        ("centers", Filter.union(centers.values())),
        ("cross", cross),
    ]


def cfop_f2l_a_2() -> list[tuple[str, Filter]]:
    cross = Filter.union(ridges.values()) & cells[BASE]
    # RU + LU
    # RD + LD
    # UF + UB
    # DF + DB
    return [
        ("centers", Filter.union(centers.values())),
        ("cross", cross),
    ]


def cfop_f2l_a_4() -> list[tuple[str, Filter]]:
    cross = Filter.union(ridges.values()) & cells[BASE]
    cross |= Filter.union(centers.values()) - cells[TOP]
    # white/yellow on I, pairs in P slice
    f2l_a_4 = EVERYTHING - cells[TOP] - cells["U"] - cells["D"]
    f2l_a_4 |= cross
    # red/orange on I, pairs in P slice
    f2l_a_8 = EVERYTHING - cells[TOP] - cells["R"] - cells["L"]
    f2l_a_8 |= f2l_a_4
    # green/blue on I, pairs in P slice
    f2l_a_12 = EVERYTHING - cells[TOP] - cells["F"] - cells["B"]
    f2l_a_12 |= f2l_a_8
    return [
        ("centers", Filter.union(centers.values())),
        ("cross", cross),
        ("f2l-a 4", f2l_a_4),
        ("f2l-a 8", f2l_a_8),
        ("f2l-a 12", f2l_a_12),
    ]


def cfop_f2l_b() -> list[tuple[str, Filter]]:
    acc = Filter.union(ridges.values()) & cells[BASE]
    acc |= Filter.union(centers.values()) - cells[TOP]
    acc |= Filter.union(pairs_a.values())
    ret = []
    for name, filter in pairs_b.items():
        acc |= filter
        ret.append((name, acc))
    return ret


def ll() -> list[tuple[str, Filter]]:
    # TODO: generate this programmatically
    return [
        ("olc 2c", Filter("01471400000000000000")),
        ("olc 3c", Filter("aaa8aa20000000000000")),
        ("olc 4c", Filter("54104150000000000000")),
        ("plc 2c", Filter("014714080a5010004000")),
        ("plc cross", Filter("01459e20000000000000")),
        ("plc f2l", Filter("00efff70000000000000")),
        ("plc ll", Filter("ffffff70000000000000")),
        ("end", Filter("ffffffffffffffffffff")),
    ]


with open("temp.yaml", "w") as f:
    write_sequence(
        f,
        [*cfop_f2l_a_4(), *cfop_f2l_b(), *ll()],
    )

# with open("temp.yaml", "w") as f:
#     write_sequence(
#         f,
#         [
#             *(("cell-" + name, filter) for name, filter in cells.items()),
#             *(("center-" + name, filter) for name, filter in centers.items()),
#             *(("ridge-" + name, filter) for name, filter in ridges.items()),
#             *(("edge-" + name, filter) for name, filter in edges.items()),
#             *(("corner-" + name, filter) for name, filter in corners.items()),
#             *(("pairs_a-" + name, filter) for name, filter in pairs_a.items()),
#             *(("pairs_b-" + name, filter) for name, filter in pairs_b.items()),
#         ],
#     )
