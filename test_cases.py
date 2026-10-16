"""Runs every required test case from the assignment and checks the answers.

Usage:  python test_cases.py
"""

from delivery import from_pairs
from scheduling import is_compatible, max_deliveries_one_driver, min_drivers, min_rejections

TASK_A = [
    ([], 0),
    ([(1, 3)], 1),
    ([(1, 3), (3, 5), (5, 7)], 3),
    ([(1, 5), (2, 6), (3, 7)], 1),
    ([(5, 7), (1, 3), (3, 5), (2, 4)], 3),
    ([(1, 4), (2, 4), (4, 6)], 2),
]

TASK_B = [
    ([], 0),
    ([(1, 3)], 1),
    ([(1, 3), (3, 5), (5, 7)], 1),
    ([(1, 5), (2, 6), (3, 7)], 3),
    ([(1, 4), (2, 5), (4, 7), (5, 8)], 2),
    ([(5, 8), (1, 4), (2, 5), (4, 6), (6, 9)], 2),
]

TASK_C = [
    ([], 0),
    ([(1, 3)], 0),
    ([(1, 3), (3, 5), (5, 7)], 0),
    ([(1, 5), (2, 6), (3, 7)], 2),
    ([(5, 7), (1, 3), (3, 5), (2, 4)], 1),
    ([(1, 2), (2, 3), (3, 4), (1, 3)], 1),
]


def fmt(ds) -> str:
    return " ".join(f"{d.id}({d.start},{d.finish})" for d in ds) or "-"


def run() -> bool:
    ok = True

    print("Task A: Maximum deliveries for one driver")
    for i, (pairs, expected) in enumerate(TASK_A, start=1):
        sel = max_deliveries_one_driver(from_pairs(pairs))
        passed = len(sel) == expected and is_compatible(sel)
        ok &= passed
        print(f"  Test {i}: expected {expected}, got {len(sel)}  selected: {fmt(sel)}  "
              f"{'PASS' if passed else 'FAIL'}")

    print("\nTask B: Minimum number of drivers")
    for i, (pairs, expected) in enumerate(TASK_B, start=1):
        ds = from_pairs(pairs)
        scheds = min_drivers(ds)
        all_assigned = sorted(d.id for s in scheds for d in s) == sorted(d.id for d in ds)
        passed = len(scheds) == expected and all_assigned and all(map(is_compatible, scheds))
        ok &= passed
        layout = "; ".join(f"Driver {j}: {fmt(s)}" for j, s in enumerate(scheds, 1)) or "-"
        print(f"  Test {i}: expected {expected}, got {len(scheds)}  {layout}  "
              f"{'PASS' if passed else 'FAIL'}")

    print("\nTask C: Minimum rejections")
    for i, (pairs, expected) in enumerate(TASK_C, start=1):
        count, rejected = min_rejections(from_pairs(pairs))
        passed = count == expected
        ok &= passed
        print(f"  Test {i}: expected {expected}, got {count}  rejected: {fmt(rejected)}  "
              f"{'PASS' if passed else 'FAIL'}")

    print("\nALL TESTS PASSED" if ok else "\nSOME TESTS FAILED")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
