#!/usr/bin/env python3
"""
Usage:
    python terminal_visualize.py UP
"""

import sys
from trend_symbols import TREND_SYMBOLS  # your file


def print_symbol(name, size=8):
    name = name.upper()
    if name not in TREND_SYMBOLS:
        print(f"Symbol '{name}' not found.")
        print("Available:", ", ".join(TREND_SYMBOLS.keys()))
        return

    coords = TREND_SYMBOLS[name]

    # Create empty 8x8 matrix
    grid = [[" . " for _ in range(size)] for _ in range(size)]

    # Fill coordinates (y is row, x is col)
    for x, y in coords:
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = " # "

    # Print grid row by row (top row first)
    print(f"\n{ name } :\n")
    for row in grid:
        print("".join(row))
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python terminal_visualize.py SYMBOL_NAME")
        sys.exit(1)

    print_symbol(sys.argv[1])
