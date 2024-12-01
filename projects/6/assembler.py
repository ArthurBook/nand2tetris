#!/usr/bin/env python3

from typing import Iterator, Mapping
import itertools
import dataclasses
import logging
import pathlib
import argparse
import enum


LOG_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


class Syntax(str, enum.Enum):
    A_INSTRUCTION = '@'
    COMMENT = '//'
    WRITE = '='
    JMP = ';'
    SYMBOL_START = '('
    SYMBOL_END = ')'


PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
    **{f"R{i}": i for i in range(16)},
}
COMP_MAP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010", "D-A": "0010011",
    "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000", "D|A": "0010101",
    "D|M": "1010101"
}
DEST_MAP = {
    '': "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}
JUMP_MAP = {
    '': "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


@dataclasses.dataclass(frozen=True)
class Config:
    src: pathlib.Path
    out: pathlib.Path
    verbosity: int


def main() -> None:
    cnf = parse_config()
    configure_logging(cnf.verbosity)
    compile_asm(cnf)


def parse_config() -> Config:
    argparser = argparse.ArgumentParser(description="Assemble an .asm file.")
    argparser.add_argument("-s", "--src", required=True,
                           help="Path to the .asm source file to compile.")
    argparser.add_argument("-o", "--out", required=False,
                           help="Path of the resulting .hack binary.")
    argparser.add_argument("-v", "--verbose", action="count", default=0,
                           help="Verbosity level (e.g., -v, -vv, -vvv).")
    args = argparser.parse_args()
    assert pathlib.Path(args.src).exists(), f"Unknown {args.src=}"
    assert args.verbose in LOG_LEVELS, f'Unknown {args.verbose=}'
    return Config(
        src=pathlib.Path(args.src),
        out=pathlib.Path(args.out or args.src.rsplit('.', 1)[0] + '.hack'),
        verbosity=LOG_LEVELS[args.verbose],
    )


def configure_logging(log_level: int):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.debug("Logging configured with verbosity level %d", log_level)


def compile_asm(cnf: Config) -> None:
    parsed_lines = _scan(cnf.src)
    n_lines = 0
    with cnf.out.open('w') as out:
        for bus in _compile(parsed_lines):
            out.write(f'{bus:016b}\n')
            n_lines += 1
    logging.info('wrote %i lines of machine code to %s', n_lines, cnf.out)


def _scan(src: pathlib.Path) -> list[str]:
    raw_lines = src.read_text().split('\n')
    logging.info('Read %i lines from %s.', len(raw_lines), src)
    parsed_lines = [
        pline for line in raw_lines
        if (pline := line.split(Syntax.COMMENT, 1)[0].strip().replace(' ', ''))
    ]
    logging.info('%i lines after lexing', len(parsed_lines))
    return parsed_lines


def _compile(parsed_lines: list[str]) -> Iterator[int]:
    address_map = _collect_symbol_addresses(parsed_lines)
    for line in itertools.filterfalse(_is_symbol, parsed_lines):
        yield (
            _parse_a_instruction(line, address_map)
            if _is_a_instruction(line)
            else _parse_c_instruction(line)
        )


def _collect_symbol_addresses(parsed_lines: list[str]) -> dict[str, int]:
    address_map = PREDEFINED_SYMBOLS.copy()
    address = 0
    for line in parsed_lines:
        if _is_symbol(line):
            symbol = _parse_symbol(line)
            assert symbol not in address_map, f"duplicate {symbol=}"
            address_map[symbol] = address
        else:
            address += 1
    return address_map


def _is_symbol(line: str) -> bool:
    return (
        line.startswith(Syntax.SYMBOL_START)
        and line.endswith(Syntax.SYMBOL_END)
    )


def _parse_symbol(line: str) -> str:
    return line.strip(Syntax.SYMBOL_START +
                      Syntax.SYMBOL_END)


def _is_a_instruction(parsed_line: str) -> bool:
    return parsed_line.startswith(Syntax.A_INSTRUCTION)


def _parse_a_instruction(line: str, address_map: dict[str, int]) -> int:
    symbol = line[1:]
    address = _resolve_address(symbol, address_map)
    binary = int(f'0{address:015b}', 2)
    logging.debug('Parsed A-instruction: %-10s -> %s', line, f'{binary:016b}')
    return binary


def _resolve_address(symbol: str, address_map: dict[str, int]) -> int:
    if symbol.isdigit():
        return int(symbol)
    if symbol not in address_map:
        address_map[symbol] = len(address_map)  # Allocate new address
    address = address_map[symbol]
    logging.debug('Resolved symbol %s to address %i', symbol, address)
    return address


def _parse_c_instruction(line: str) -> int:
    if Syntax.WRITE in line:
        dest, comp_jump = line.split(Syntax.WRITE)
    else:
        dest, comp_jump = '', line
    if Syntax.JMP in comp_jump:
        comp, jump = comp_jump.split(Syntax.JMP)
    else:
        comp, jump = comp_jump, ''
    binary = int(f"111{COMP_MAP[comp]}{DEST_MAP[dest]}{JUMP_MAP[jump]}", 2)
    logging.debug('Parsed C-instruction: %-10s -> %s', line, f'{binary:016b}')
    return binary


if __name__ == '__main__':
    main()
