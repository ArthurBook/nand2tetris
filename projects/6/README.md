# Assembler
The assembler is written in python with a small Command Line Interface (CLI).
To read more about the CLI, run `assembler.py --help`.

## Example compile of `Add.asm` file
```bash
 ❯ projects/6/assembler.py -s projects/6/add/Add.asm -vv
2024-12-01 13:39:20,987 - DEBUG - Logging configured with verbosity level 10
2024-12-01 13:39:20,987 - INFO - Read 14 lines from projects/6/add/Add.asm.
2024-12-01 13:39:20,987 - INFO - 6 lines after lexing
2024-12-01 13:39:20,988 - DEBUG - Parsed A-instruction: @2         -> 0000000000000010
2024-12-01 13:39:20,988 - DEBUG - Parsed C-instruction: D=A        -> 1110110000010000
2024-12-01 13:39:20,988 - DEBUG - Parsed A-instruction: @3         -> 0000000000000011
2024-12-01 13:39:20,988 - DEBUG - Parsed C-instruction: D=D+A      -> 1110000010010000
2024-12-01 13:39:20,988 - DEBUG - Parsed A-instruction: @0         -> 0000000000000000
2024-12-01 13:39:20,988 - DEBUG - Parsed C-instruction: M=D        -> 1110001100001000
2024-12-01 13:39:20,988 - INFO - wrote 6 lines of machine code to projects/6/add/Add.hack
```
```
```
