def search_range(x: str, r: tuple[int, int], y: str, j: int) -> int:
    """
    Takes two strings to compare, a range to look through on one string and an index to start at on the other string.
    Returns how many comparisons were made before either a mismatch or the end of a string was reached.
    """
    i, m = r
    length = min(m - i, len(y) - j)
    for k in range(length):
        if x[i + k] != y[j + k]:
            return k
    return length
