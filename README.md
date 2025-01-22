# Python-Sudoku-Algorithm

## Summary:

A short python program that can output the solution of a given solvable sudoku puzzle

Using a series of logical algorithms and a bit of brute force, this program is able to solve just about any solvable sudoku puzzle.

To prove its effectiveness, it has been tested with a list of 100,000+ difficult puzzles (contained in "diabolical.txt"). The solutions for those puzzles were written into another file (contained in "solutions.txt").

The "diabolical" file is borrowed from grantm's giant text file of diabolical-difficulty puzzles: https://github.com/grantm/sudoku-exchange-puzzle-bank

## Usage:

When using the program, you can either:

1. Input your own custom sudoku puzzle as an 81-digit string.
2. Tell the program to solve a specified range of puzzles from the attached puzzles file.
3. Tell the program to read from the puzzles file and write the solutions to the "solutions" text file. This file is already full; this is what I used to fill it out. If one were to erase any number of lines from the end of the solutions file, they could use this function to fill the rest of it out.

When you command the program to solve a sudoku, you may choose either to see just the results of the whole process, the resulting solution for every inputted puzzle, or to see the full incremental process of solving each puzzle.

## Logic:

The algorithm uses several different logical rules to solve the puzzles. These rules were determined using the basic rules of sudoku, with each row, column, and 3x3 region being required to contain exactly 1 of every 1-9 value.

The algorithm uses a "confusion" value to increase solving speed. At confusion 0, it applies the fastest and most broadly-applicable rules first. If it cannot make any progress through those, the "confusion" counter increases, meaning it will apply more complex rules to the puzzle. If the logical rules are all unsuccessful, it will then attempt to solve the sudoku through sheer brute force. If at any point it makes some amount of progress, its confusion will reset, as it is likely that the simpler rules may be able to make further progress.

The program usually takes about 0.03-0.10 seconds to solve a puzzle. This tends to vary based on the difficulty of the puzzle; harder puzzles give less information and thus require slower and more complicated methods to solve.
