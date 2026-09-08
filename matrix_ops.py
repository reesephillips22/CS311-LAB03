"""
Lab 3: The Row-Major Detective -- starter.

Complete the two functions below. See
Lab_03_The_Row_Major_Detective.md, Part B, for the full requirements.
"""

from typing import List


def transpose_inplace(matrix: List[List[float]]) -> None:
    """
    Transpose a SQUARE matrix in place (no new matrix allocated).
    Mutates `matrix` directly; returns None.
    """
    n = len(matrix)
    for r in range(n):
            for c in range(r + 1, n):
                matrix[r][c], matrix [c][r] = matrix[c][r], matrix[r][c]


def transpose_blocked(matrix: List[List[float]], block_size: int) -> List[List[float]]:
    """
    Transpose a (possibly non-square) matrix using a blocked/tiled
    access pattern for cache locality, returning a NEW matrix.
    """
    rows = len(matrix)
    if rows == 0:
        return []
    
    cols = len(matrix[0])
    if cols == 0:
        return []

    result = [[0.0] * rows for _ in range(cols)]

    for r0 in range(0, rows, block_size):
        r1 = min(r0 + block_size, rows)

        for c0 in range(0, cols, block_size):
            c1 = min(c0 + block_size, cols)

            block = zip(*(row[c0:c1] for row in matrix[r0:r1]))

            for offset, transposed_row in enumerate(block):
                result[c0 + offset][r0:r1] = transposed_row
    return result
