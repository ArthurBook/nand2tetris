#!/usr/bin/env python3

import argparse
import dataclasses
import enum
import logging
import pathlib
from typing import List, Literal, Optional


class GlobalCounter:
    _count: int = 0

    @classmethod
    def incr(cls) -> int:
        cls._count += 1
        return cls._count


LOG_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


class Syntax(str, enum.Enum):
    COMMENT = "//"


class Segment(str, enum.Enum):
    LCL = "local"
    ARG = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    STATIC = "static"
    STACK = "stack"
    CONSTANT = "constant"
    POINTER = "pointer"


class Method(str, enum.Enum):
    PUSH = "push"
    POP = "pop"


class Op(str, enum.Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


STANDARD_VM_MAPPING = {
    Segment.LCL: 1,
    Segment.ARG: 2,
    Segment.THIS: 3,
    Segment.THAT: 4,
    Segment.TEMP: 5,
    Segment.STATIC: 16,
    Segment.STACK: 256,  # Up to 2047 (inclusive)
}


@dataclasses.dataclass(frozen=True)
class Config:
    src: pathlib.Path
    out: pathlib.Path
    log_verbosity: int


def main() -> None:
    cnf = parse_config()
    configure_logging(cnf.log_verbosity)
    translate_vmcode(cnf)


def parse_config() -> Config:
    argparser = argparse.ArgumentParser(description="Translate a .vm file.")
    argparser.add_argument("src", help="Path to the .vm source file to compile.")
    argparser.add_argument("-o", "--out", required=False, help="Path of the resulting .asm assembly code.")
    argparser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity level (e.g., -v, -vv, -vvv).",
    )
    args = argparser.parse_args()
    assert pathlib.Path(args.src).exists(), f"Unknown {args.src=}"
    assert args.verbose in LOG_LEVELS, f"Unknown {args.verbose=}"

    return Config(
        src=pathlib.Path(args.src),
        out=pathlib.Path(args.src.rsplit(".", 1)[0] + ".asm"),
        log_verbosity=LOG_LEVELS[args.verbose],
    )


def configure_logging(log_level: int):
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Logging configured with verbosity level %d", log_level)


def translate_vmcode(cnf: Config) -> None:
    n_lines = 0
    with cnf.src.open("r") as file:
        with cnf.out.open("w") as out:
            for stmnt in filter(None, map(_translate_line, file)):
                out.write(f"{stmnt}\n")
                n_lines += 1
    logging.info("wrote %i statements of assembly to %s", n_lines, cnf.out)


def _translate_line(line: str) -> Optional[str]:
    if not (lexed_line := line.split(Syntax.COMMENT, 1)[0].strip().lower()):
        return None
    parts = lexed_line.split()
    if len(parts) == 1:
        stmnt = _translate_arithmetic(Op(parts[0]))
    elif len(parts) == 3:
        stmnt = _translate_memaccess(Method(parts[0]), Segment(parts[1]), int(parts[2]))
    else:
        raise SyntaxError(f"Unknown line: {line}")
    tranlated = "\n".join(("// " + line.rstrip("\n"), *stmnt))
    logging.debug("\n%s\n", tranlated)
    return tranlated


def _translate_arithmetic(op: Op) -> List[str]:
    if op is Op.NOT:
        return _unaryop("!")
    if op is Op.NEG:
        return _unaryop("-")
    if op is Op.ADD:
        return _binaryop("+")
    if op is Op.SUB:
        return _binaryop("-")
    if op is Op.AND:
        return _binaryop("&")
    if op is Op.OR:
        return _binaryop("|")
    if op is Op.EQ:
        return _logicalop("JEQ")
    if op is Op.GT:
        return _logicalop("JGT")
    if op is Op.LT:
        return _logicalop("JLT")
    raise SyntaxError(f"Unknown arithmetic operation: {op}")


def _translate_memaccess(method: Method, segment: Segment, index: int) -> List[str]:
    if method == Method.PUSH and segment == Segment.CONSTANT:
        return [f"@{index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif method == Method.PUSH and segment in {Segment.LCL, Segment.ARG, Segment.THIS, Segment.THAT}:
        return  _push_base_seg(segment, index)
    elif method == Method.PUSH and segment in {Segment.TEMP, Segment.STATIC}:
        return _push_to(STANDARD_VM_MAPPING[segment] + index)
    elif method == Method.PUSH and segment == Segment.POINTER:
        return _push_to(STANDARD_VM_MAPPING[Segment.THIS] + index)
    elif method == Method.POP and segment in (Segment.LCL, Segment.ARG, Segment.THIS, Segment.THAT):
        return __pop_base_seg(segment, index)
    elif method == Method.POP and segment in {Segment.TEMP, Segment.STATIC}:
        return _pop_at(STANDARD_VM_MAPPING[segment] + index)
    elif method == Method.POP and segment == Segment.POINTER:
        return _pop_at(STANDARD_VM_MAPPING[Segment.THIS] + index)
    raise SyntaxError(f"Unknown memory access: {method} {segment} {index}")



def _unaryop(op: Literal["-", "!"]) -> List[str]:
    return ["@SP", "A=M-1", f"M={op}M"]


def _binaryop(op: Literal["+", "-", "&", "|"]) -> List[str]:
    return ["@SP", "AM=M-1", "D=M", "A=A-1", f"M=M{op}D"]


def _logicalop(op: Literal["JEQ", "JGT", "JLT"]) -> List[str]:
    symbol = f"COMP_{op}_{GlobalCounter.incr()}"
    return [
        "@SP",
        "AM=M-1",
        "D=M",  # Pop y into D
        "A=A-1",
        "D=M-D",  # Pop x, compute x-y
        f"@{symbol}_TRUE",
        f"D;{op}",  # If true, jump to TRUE
        "@SP",
        "A=M-1",
        "M=0",  # Else, set top of stack to 0 (false)
        f"@{symbol}_END",
        "0;JMP",  # Jump to END
        f"({symbol}_TRUE)",
        "@SP",
        "A=M-1",
        "M=-1",  # TRUE: set top of stack to -1
        f"({symbol}_END)",
    ]


def _push_to(index: int) -> List[str]:
    return [f"@{index}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]


def _push_base_seg(segment: Segment, index: int) -> List[str]:
    return [
        f"@{index}",
        "D=A",
        f"@{STANDARD_VM_MAPPING[segment]}",
        "A=M+D",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def _pop_at(index: int) -> List[str]:
    return ["@SP", "AM=M-1", "D=M", f"@{index}", "M=D"]


def __pop_base_seg(segment: Segment, index: int) -> List[str]:
    return [
        f"@{index}",
        "D=A",
        f"@{STANDARD_VM_MAPPING[segment]}",
        "D=M+D",
        "@R13",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@R13",
        "A=M",
        "M=D",
    ]

if __name__ == "__main__":
    main()
