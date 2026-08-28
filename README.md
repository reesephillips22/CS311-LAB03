# Lab 3: The Row-Major Detective

Full assignment: `Lab_03_The_Row_Major_Detective.md`.

## Run
```bash
python benchmark_matrix.py
```
Complete `matrix_ops.py`. The script checks correctness first, then
benchmarks `transpose_blocked` against a naive baseline on a 1000x1000
matrix -- it must be at least 1.5x faster. Success Token prints on a
full pass.

## Instructor note (resolved 2026-08-27)
The prompt's old Requirement 2 required the block working buffer to
be backed by `array.array`. Verified by benchmark: that makes things
*slower*, not faster (0.6-0.9x vs. naive) -- per-element conversion
overhead outweighs the cache-locality gain at this scale in pure
Python. A plain-nested-list blocked transpose reliably clears the
1.5x bar at block_size=32 (measured 1.6-2.2x across block sizes in
testing). `Lab_03_The_Row_Major_Detective.md`/`.docx` Requirement 2
has been reworded to drop the `array.array` requirement and explain
why -- the interpreter-overhead-hides-hardware-effects point is
itself worth teaching. 1.5x threshold left as-is; it's realistic now.

## Submit
1. `Lab3_Theory.pdf` (or `.md`)
2. `matrix_ops.py`
3. The Success Token
