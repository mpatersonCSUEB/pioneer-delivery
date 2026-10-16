# Pioneer Delivery Algorithm Portfolio — Part I: Greedy Algorithms

CS 413 — Analysis of Algorithms

## Language

Python 3.10+ (standard library only — `heapq`, `dataclasses`, `fractions`, `itertools`).

## AI Usage

Claude was used to brainstorm a solution that fits the project's requirements, and to implement the solution in Python. The code was reviewed and the outputs were measured to ensure the correct outcome is met.

## How to run

No compilation step is needed.

```bash
# Run Tasks A, B and C on a delivery file
python3 main.py deliveries.txt

# Run every required test case from the assignment (prints PASS/FAIL)
python3 test_cases.py

# Task D: show the greedy counterexample and verify it by brute force
python3 greedy_counterexample.py
```

## Input file format

One delivery per line: `id start_time finish_time`, separated by whitespace.
Times are integers with `start < finish`. Blank lines and lines beginning with
`#` are ignored. A delivery finishing at time `t` is compatible with one
starting at `t`.

Sample file (`deliveries.txt`):

```
D01 10 13
D02 2 5
D03 4 7
D04 1 8
D05 8 11
D06 11 14
D07 13 16
```

## Program organization

| File | Contents |
|---|---|
| `delivery.py` | `Delivery` data class, `load_deliveries()` file parser, `from_pairs()` helper for tests |
| `scheduling.py` | `max_deliveries_one_driver()` (Task A), `min_drivers()` (Task B), `min_rejections()` (Task C), `is_compatible()` checker |
| `main.py` | Command-line entry point; reads a file and prints the output of Tasks A–C |
| `test_cases.py` | All required test cases for Tasks A–C, with automatic correctness checks |
| `greedy_counterexample.py` | Task D counterexample, greedy simulation, and brute-force optimum |
| `deliveries.txt` | Sample data file |

---

## Task A — Maximum deliveries for one driver

**Algorithm.** Sort deliveries by finish time. Scan them in that order, keeping
the finish time of the last selected delivery. Select a delivery whenever its
start time is ≥ that finish time.

**1. Greedy choice.** My algorithm will choose deliviers with the earliest start time.

**2. Why it is optimal (exchange argument).** Let `g₁, g₂, …, g_k` be the greedy
selections and `o₁, o₂, …, o_m` an optimal schedule, both sorted by finish time.
By induction, `finish(gᵢ) ≤ finish(oᵢ)` for every `i ≤ k` ("greedy stays
ahead"): for `i = 1` greedy picked the earliest finish overall; if it holds for
`i − 1`, then `oᵢ` starts after `o_{i−1}` finishes, hence after `g_{i−1}`
finishes, so `oᵢ` was available to greedy, and greedy chose something finishing
no later. If `m > k`, then `o_{k+1}` starts after `o_k` finishes ≥ after `g_k`
finishes, so greedy would still have had a compatible delivery and would not
have stopped at `k` — a contradiction. So `k = m`. Equivalently: replacing the
first delivery of any optimal schedule with the earliest-finishing one never
creates a conflict, so some optimal schedule begins with the greedy choice, and
the same reasoning applies to the remaining subproblem.

**3. Running time.** Sorting is `O(n log n)` and the scan is `O(n)`, The total is
`O((n log n) + n)`.

## Task B — Minimum number of drivers

**Algorithm.** Sort deliveries by start time. Maintain a min-heap with one entry
per driver hired so far. For each delivery, look at the top of the heap: if that
driver is free by the delivery's start time, pop them and assign the delivery;
otherwise hire a new driver. Push the assigned driver back with the delivery's
finish time.

**1. What Information is stored in the priority queue?** Pairs `(free_at, driver_index)` — the
time each driver finishes their most recent delivery — keyed on `free_at`, so the
top is the driver who becomes available soonest.

**2. How is a driver selected for each new delivery?** The new delivery goes to the driver at the top
of the heap if `free_at ≤ start`; if even that driver is still busy, every
driver is busy, so a new driver is created.

**3. Why does this algorithm use the minimum possible number of drivers?** Define the *depth* `d` as the
maximum number of deliveries in progress at any single moment. Any valid
schedule needs at least `d` drivers. The algorithm only hires driver number
`k` when a delivery starting at time `s` finds all `k − 1` existing drivers busy
at `s` — each of them is working a delivery that started at or before `s`
(because we process by start time) and finishes after `s`. Together with the new
delivery, that is `k` deliveries overlapping at time `s`, so `k ≤ d`. The
algorithm therefore uses exactly `d` drivers, which matches the lower bound.
No driver receives overlapping deliveries because a driver is reused only when
`free_at ≤ start`.

**4. What is the running time?** Sorting is `O(n log n)`. Each delivery does at most one
pop and one push on a heap of size ≤ `n`, `O(log n)` each, so the total
**`O(n log n)`**.

## Task C — Minimum rejections (one driver)

**1. How is this problem related to Task A?** Rejecting the fewest deliveries is the same as
keeping the most. The deliveries we keep must be mutually compatible, so the
best we can keep is exactly the Task A answer. `min_rejections()` calls Task A
and returns everything not selected.

**2. f the maximum number of compatible deliveries is k, how many deliveries must be rejected?** If the maximum number of compatible deliveries is `k`,
the minimum number rejected is **`n − k`**.

**3. What is the running time of your algorithm?** One call to Task A (`O(n log n)`) plus an `O(n)` pass to
list the rejected deliveries, so the total is **`O(n log n)`**.

## Task D — When a greedy choice fails

Value of delivery `j` in slot `T`: `V_j = P_j / (1 + (T − R_j))`.

**1. Instance.**

| Delivery | Ready time `R` | Profit `P` |
|---|---|---|
| A | 0 | 10 |
| B | 0 | 9 |
| C | 1 | 8 |

**2. Greedy schedule G** (decreasing profit, earliest open slot ≥ `R`):

| Delivery | Slot | Delay | Value |
|---|---|---|---|
| A | 0 | 0 | 10/1 = 10 |
| B | 1 | 1 | 9/2 = 4.5 |
| C | 2 | 1 | 8/2 = 4 |

`V(G) = 10 + 4.5 + 4 = 18.5`

**3. Better schedule S:**

| Delivery | Slot | Delay | Value |
|---|---|---|---|
| A | 0 | 0 | 10/1 = 10 |
| C | 1 | 0 | 8/1 = 8 |
| B | 2 | 2 | 9/3 = 3 |

`V(S) = 10 + 8 + 3 = 21`

**4. Why this proves G is not always optimal.** `S` is a valid schedule
(every slot is ≥ the ready time and no two deliveries share a slot) and
`V(S) = 21 > 18.5 = V(G)`. A single instance where G's output is beaten is
enough to show G is not optimal in general. The failure comes from G ignoring
ready times: it gives slot 1 to B because B has the higher profit, but C is
*only* able to use slot 1 without delay, while B is already delayed no matter
what. Putting C in slot 1 saves 4 units of C's value and costs only 1.5 units of
B's. `greedy_counterexample.py` reproduces G and confirms by exhaustive search
that 21 is the true optimum for this instance.

---

## Required test results

Output of `python3 test_cases.py`:

```
Task A: Maximum deliveries for one driver
  Test 1: expected 0, got 0  selected: -  PASS
  Test 2: expected 1, got 1  selected: D1(1,3)  PASS
  Test 3: expected 3, got 3  selected: D1(1,3) D2(3,5) D3(5,7)  PASS
  Test 4: expected 1, got 1  selected: D1(1,5)  PASS
  Test 5: expected 3, got 3  selected: D2(1,3) D3(3,5) D1(5,7)  PASS
  Test 6: expected 2, got 2  selected: D1(1,4) D3(4,6)  PASS

Task B: Minimum number of drivers
  Test 1: expected 0, got 0  -  PASS
  Test 2: expected 1, got 1  Driver 1: D1(1,3)  PASS
  Test 3: expected 1, got 1  Driver 1: D1(1,3) D2(3,5) D3(5,7)  PASS
  Test 4: expected 3, got 3  Driver 1: D1(1,5); Driver 2: D2(2,6); Driver 3: D3(3,7)  PASS
  Test 5: expected 2, got 2  Driver 1: D1(1,4) D3(4,7); Driver 2: D2(2,5) D4(5,8)  PASS
  Test 6: expected 2, got 2  Driver 1: D2(1,4) D4(4,6) D5(6,9); Driver 2: D3(2,5) D1(5,8)  PASS

Task C: Minimum rejections
  Test 1: expected 0, got 0  rejected: -  PASS
  Test 2: expected 0, got 0  rejected: -  PASS
  Test 3: expected 0, got 0  rejected: -  PASS
  Test 4: expected 2, got 2  rejected: D2(2,6) D3(3,7)  PASS
  Test 5: expected 1, got 1  rejected: D4(2,4)  PASS
  Test 6: expected 1, got 1  rejected: D4(1,3)  PASS

ALL TESTS PASSED
```

In the tests, deliveries are auto-named `D1, D2, …` in the order listed in the
assignment table.

Output of `python3 main.py deliveries.txt`:

```
=== Task A: Maximum deliveries for one driver ===
  D02    start=2    finish=5
  D05    start=8    finish=11
  D06    start=11   finish=14
Total deliveries completed: 3

=== Task B: Minimum number of drivers ===
  Driver 1: D04 D06
  Driver 2: D02 D05 D07
  Driver 3: D03 D01
Minimum drivers required: 3

=== Task C: Minimum rejections (one driver) ===
  Rejected: D01 D03 D04 D07
Minimum deliveries rejected: 4
```
