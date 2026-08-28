"""
Lab 3: The Row-Major Detective -- verification suite.

Run: python benchmark_matrix.py
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import random
import sys
import timeit
from typing import List

from matrix_ops import transpose_blocked, transpose_inplace

ASSIGNMENT_ID = "LAB03"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def naive_transpose(matrix: List[List[float]]) -> List[List[float]]:
    """Reference baseline: the obvious nested-loop transpose."""
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def make_matrix(rows: int, cols: int) -> List[List[float]]:
    return [[random.random() for _ in range(cols)] for _ in range(rows)]


def main() -> int:
    failures: list = []

    print("Verifying correctness on small matrices...\n")

    square = make_matrix(20, 20)
    expected_square = naive_transpose([row[:] for row in square])
    working_copy = [row[:] for row in square]
    transpose_inplace(working_copy)
    check("transpose_inplace matches naive transpose on a square matrix", working_copy == expected_square, failures)

    rect = make_matrix(30, 12)
    expected_rect = naive_transpose(rect)
    blocked_result = transpose_blocked(rect, block_size=4)
    check("transpose_blocked matches naive transpose on a non-square matrix", blocked_result == expected_rect, failures)

    if failures:
        print(f"\n{len(failures)} correctness check(s) failed -- fix these before benchmarking. No token issued.")
        return 1

    print("\nBenchmarking on a 1000x1000 matrix...\n")
    big = make_matrix(1000, 1000)

    naive_time = timeit.timeit(lambda: naive_transpose(big), number=3) / 3
    blocked_time = timeit.timeit(lambda: transpose_blocked(big, block_size=32), number=3) / 3
    speedup = naive_time / blocked_time if blocked_time > 0 else 0.0

    print(f"  naive transpose:   {naive_time:.4f}s (avg of 3)")
    print(f"  blocked transpose: {blocked_time:.4f}s (avg of 3)")
    print(f"  speedup:           {speedup:.2f}x\n")

    check("transpose_blocked is at least 1.5x faster than naive on 1000x1000", speedup >= 1.5, failures)

    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
