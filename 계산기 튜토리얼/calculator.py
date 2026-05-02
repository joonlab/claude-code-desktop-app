"""간단한 파이썬 계산기.

사칙연산과 거듭제곱, 나머지 연산을 지원합니다. 0으로 나누는 경우와
지원하지 않는 연산자는 명시적인 예외를 발생시킵니다.
"""

from __future__ import annotations

from typing import Callable

Number = float | int


def add(a: Number, b: Number) -> Number:
    return a + b


def subtract(a: Number, b: Number) -> Number:
    return a - b


def multiply(a: Number, b: Number) -> Number:
    return a * b


def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b


def power(a: Number, b: Number) -> Number:
    return a ** b


def modulo(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("0으로 나머지 연산을 할 수 없습니다.")
    return a % b


OPERATIONS: dict[str, Callable[[Number, Number], Number]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
    "%": modulo,
}


def calculate(a: Number, op: str, b: Number) -> Number:
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자: {op!r}")
    return OPERATIONS[op](a, b)


if __name__ == "__main__":
    demo = [
        (12, "+", 30),
        (100, "-", 47),
        (8, "*", 9),
        (144, "/", 12),
        (2, "**", 10),
        (37, "%", 5),
    ]
    for a, op, b in demo:
        print(f"{a} {op} {b} = {calculate(a, op, b)}")
