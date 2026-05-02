"""calculator.py에 대한 샌드박스 검증 스크립트."""

from __future__ import annotations

import math
import time
import traceback
from dataclasses import dataclass

from calculator import calculate


@dataclass
class TestCase:
    name: str
    func: callable
    expected: object


def expect_equal(actual, expected) -> bool:
    if isinstance(expected, float) and isinstance(actual, float):
        return math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    return actual == expected


def expect_raises(exc_type, func) -> bool:
    try:
        func()
    except exc_type:
        return True
    except Exception:
        return False
    return False


def main() -> int:
    cases: list[TestCase] = [
        TestCase("덧셈: 12 + 30", lambda: calculate(12, "+", 30), 42),
        TestCase("뺄셈: 100 - 47", lambda: calculate(100, "-", 47), 53),
        TestCase("곱셈: 8 * 9", lambda: calculate(8, "*", 9), 72),
        TestCase("나눗셈: 144 / 12", lambda: calculate(144, "/", 12), 12.0),
        TestCase("거듭제곱: 2 ** 10", lambda: calculate(2, "**", 10), 1024),
        TestCase("나머지: 37 % 5", lambda: calculate(37, "%", 5), 2),
        TestCase("음수 덧셈: -5 + 3", lambda: calculate(-5, "+", 3), -2),
        TestCase("실수 곱셈: 0.1 * 0.2", lambda: calculate(0.1, "*", 0.2), 0.02),
    ]

    error_cases: list[TestCase] = [
        TestCase("0으로 나눗셈", lambda: calculate(1, "/", 0), ZeroDivisionError),
        TestCase("0으로 나머지", lambda: calculate(1, "%", 0), ZeroDivisionError),
        TestCase("지원하지 않는 연산자", lambda: calculate(1, "??", 2), ValueError),
    ]

    passed = 0
    failed = 0
    results: list[tuple[str, str, str]] = []

    start = time.perf_counter()

    for case in cases:
        try:
            actual = case.func()
            ok = expect_equal(actual, case.expected)
            status = "PASS" if ok else "FAIL"
            detail = f"기대 {case.expected!r}, 실제 {actual!r}"
        except Exception as exc:  # noqa: BLE001
            ok = False
            status = "FAIL"
            detail = f"예외 발생: {exc!r}\n{traceback.format_exc()}"
        results.append((case.name, status, detail))
        passed += int(ok)
        failed += int(not ok)

    for case in error_cases:
        ok = expect_raises(case.expected, case.func)
        status = "PASS" if ok else "FAIL"
        detail = f"기대 예외 {case.expected.__name__}"
        results.append((case.name, status, detail))
        passed += int(ok)
        failed += int(not ok)

    elapsed_ms = (time.perf_counter() - start) * 1000

    print("=" * 60)
    print("calculator.py 샌드박스 실행 보고서")
    print("=" * 60)
    for name, status, detail in results:
        print(f"[{status}] {name} -> {detail}")
    print("-" * 60)
    print(f"총 {len(results)}건 / 통과 {passed} / 실패 {failed}")
    print(f"실행 시간: {elapsed_ms:.3f} ms")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
