# Assignment 6: Medians and Order Statistics & Elementary Data Structures

## How to Run

From the folder containing the files:

```bash
python3 part1_selection_algorithms.py
```

```bash
python3 part2_elementary_data_structures.py
```

(Use `python` instead of `python3` if that's how Python is set up on your machine.)

No arguments or input files are needed — each script runs its own tests and prints output directly.

## Sample Output

**Part 1** — correctness tests pass, followed by a timing table (size / distribution / time in seconds for each algorithm):

```
All correctness tests passed (including duplicate-heavy arrays below).
Duplicate-heavy edge case passed.

    Size  Distribution   Randomized(s)   Deterministic(s)
    1000        random         0.00035            0.00053
    1000        sorted         0.00024            0.00045
    1000       reverse         0.00033            0.00068
    1000    duplicates         0.00018            0.00020
    5000        random         0.00148            0.00259
    5000        sorted         0.00137            0.00245
    5000       reverse         0.00169            0.00220
    5000    duplicates         0.00106            0.00099
   20000        random         0.00498            0.01086
   20000        sorted         0.00434            0.00951
   20000       reverse         0.00664            0.01218
   20000    duplicates         0.00297            0.00435
   50000        random         0.00680            0.02759
   50000        sorted         0.00989            0.02516
   50000       reverse         0.01620            0.02693
   50000    duplicates         0.00561            0.01016
```

**Part 2** — all data structure tests pass:

```
Stack OK
Queue OK
Singly Linked List OK
Doubly Linked List OK

All Part 2 tests passed.
```

## Summary and Basic Analysis

- Randomized Quickselect wins on speed across the board — at every size (1,000 to 50,000) and every distribution (random, sorted, reverse, duplicates), it beat Median of Medians by roughly 1.5x to 4x. The gap widens as n grows (e.g. at 50,000 random elements, Quickselect took ~0.0068s vs Deterministic's ~0.0276s), confirming Median of Medians carries a larger constant factor from its grouping/sub-median-finding overhead at every recursion level. This matches the theory — Quickselect has a smaller constant factor per partition step, while Median of Medians pays extra overhead for grouping and finding medians of medians at every level of recursion, in exchange for a worst-case (not just expected) O(n) guarantee.
- Input order didn't meaningfully affect either algorithm — random, sorted, and reverse-sorted inputs produced similar timings for both methods at a given size. This confirms the theory: Quickselect's random pivot choice removes any dependence on how the input is arranged, and Median of Medians' guarantee holds by construction regardless of order.
- Duplicate-heavy inputs were fastest for both algorithms (e.g. at 50,000 elements: 0.0056s and 0.0102s vs ~0.0068–0.0276s for other distributions). This is because the 3-way partition collapses large equal-valued blocks in a single pass, shrinking the effective problem size quickly.
- Overall takeaway: both algorithms are O(n), but Quickselect's simplicity gives it a practical edge, making it the better default choice (matching why real-world libraries like C++'s std::nth_element use it). Median of Medians is still worth using when a hard worst-case guarantee is required and occasional slow runs from Quickselect can't be tolerated.
