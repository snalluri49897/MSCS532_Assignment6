import random
import time
import copy

# find the k-th smallest element using a 3-way partition (handles duplicates properly)
def partition_3way(arr, low, high, pivot_value):
    lt = low       # everything before lt is < pivot
    i = low        # current scanning index
    gt = high      # everything after gt is > pivot

    while i <= gt:
        if arr[i] < pivot_value:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot_value:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    return lt, gt  # range [lt, gt] all equal pivot_value


# randomized quickselect, expected O(n) time
def randomized_select(arr, low, high, k):
    if low == high:
        return arr[low]

    # pick a random pivot to avoid worst-case behavior on sorted/adversarial input
    pivot_index = random.randint(low, high)
    pivot_value = arr[pivot_index]
    lt, gt = partition_3way(arr, low, high, pivot_value)

    if lt <= k <= gt:
        return arr[k]  # k landed in the equal-to-pivot block
    elif k < lt:
        return randomized_select(arr, low, lt - 1, k)
    else:
        return randomized_select(arr, gt + 1, high, k)


def randomized_quickselect(arr, k):
    a = arr[:]  # copy so we don't mutate the caller's array
    return randomized_select(a, 0, len(a) - 1, k)


# deterministic median-of-medians, guarantees O(n) even in the worst case
def median_of_medians(arr, low, high):
    n = high - low + 1

    # base case, just sort the small chunk and grab the middle
    if n <= 5:
        sub = sorted(arr[low:high + 1])
        return sub[len(sub) // 2]

    # split into groups of 5, take the median of each group
    medians = []
    i = low
    while i <= high:
        group_end = min(i + 4, high)
        group = sorted(arr[i:group_end + 1])
        medians.append(group[len(group) // 2])
        i += 5

    # recurse to find the median of those medians, this becomes the pivot
    return deterministic_select(medians, 0, len(medians) - 1, len(medians) // 2)


def deterministic_select(arr, low, high, k):
    if low == high:
        return arr[low]

    pivot_value = median_of_medians(arr, low, high)
    lt, gt = partition_3way(arr, low, high, pivot_value)

    if lt <= k <= gt:
        return arr[k]
    elif k < lt:
        return deterministic_select(arr, low, lt - 1, k)
    else:
        return deterministic_select(arr, gt + 1, high, k)


def deterministic_selection(arr, k):
    a = arr[:]
    return deterministic_select(a, 0, len(a) - 1, k)


# quick sanity check that both algorithms agree with plain sorting
def test_correctness():
    random.seed(1)
    for trial in range(50):
        n = random.randint(1, 200)
        arr = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(0, n - 1)
        expected = sorted(arr)[k]

        got_rand = randomized_quickselect(arr, k)
        got_det = deterministic_selection(arr, k)

        assert got_rand == expected, f"Randomized failed: {arr}, k={k}"
        assert got_det == expected, f"Deterministic failed: {arr}, k={k}"

    print("All correctness tests passed (including duplicate-heavy arrays below).")

    # edge case with a lot of repeated values
    arr = [5] * 20 + [1, 2, 3]
    k = 10
    expected = sorted(arr)[k]
    assert randomized_quickselect(arr, k) == expected
    assert deterministic_selection(arr, k) == expected
    print("Duplicate-heavy edge case passed.")


# build test arrays with different shapes
def make_array(n, distribution):
    if distribution == "random":
        return [random.randint(0, 1_000_000) for _ in range(n)]
    elif distribution == "sorted":
        return list(range(n))
    elif distribution == "reverse":
        return list(range(n, 0, -1))
    elif distribution == "duplicates":
        return [random.randint(0, 10) for _ in range(n)]  # small range so lots of repeats
    else:
        raise ValueError("unknown distribution")


def time_function(func, arr, k):
    a = copy.copy(arr)
    start = time.perf_counter()
    func(a, k)
    return time.perf_counter() - start


# time both algorithms across sizes and distributions
def run_empirical_analysis():
    sizes = [1000, 5000, 20000, 50000]
    distributions = ["random", "sorted", "reverse", "duplicates"]

    print(f"\n{'Size':>8} {'Distribution':>13} {'Randomized(s)':>15} {'Deterministic(s)':>18}")
    for n in sizes:
        for dist in distributions:
            arr = make_array(n, dist)
            k = n // 2  # just find the median each time

            t_rand = time_function(randomized_quickselect, arr, k)
            t_det = time_function(deterministic_selection, arr, k)

            print(f"{n:>8} {dist:>13} {t_rand:>15.5f} {t_det:>18.5f}")


if __name__ == "__main__":
    test_correctness()
    run_empirical_analysis()