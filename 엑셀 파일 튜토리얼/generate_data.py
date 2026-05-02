"""더미 매출 데이터 생성기.

프리미엄 가전 리테일러의 2025년 연간 판매 트랜잭션을 모사한다.
시드를 고정해 동일한 데이터셋이 반복 생성되도록 한다.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

REGIONS = ["서울", "부산", "대구", "인천", "광주"]

CATALOG: dict[str, list[tuple[str, int]]] = {
    "가전": [
        ("시그니처 냉장고", 4_500_000),
        ("스타일러", 1_800_000),
        ("프리미엄 에어컨", 2_200_000),
    ],
    "모바일": [
        ("플래그십 스마트폰", 1_350_000),
        ("폴더블폰", 2_100_000),
    ],
    "노트북": [
        ("그램 17", 2_390_000),
        ("그램 프로", 3_290_000),
    ],
    "액세서리": [
        ("무선이어폰", 290_000),
        ("스마트워치", 480_000),
    ],
}

REPS = ["김민준", "이서연", "박지호", "최유나", "정도윤", "한수아"]

ROW_COUNT = 180
START = date(2025, 1, 1)
DAYS_IN_YEAR = 365


def main() -> Path:
    rows: list[dict[str, object]] = []
    for _ in range(ROW_COUNT):
        d = START + timedelta(days=random.randint(0, DAYS_IN_YEAR - 1))
        category = random.choice(list(CATALOG.keys()))
        product, unit_price = random.choice(CATALOG[category])
        units = random.randint(1, 25)
        rows.append(
            {
                "날짜": d.isoformat(),
                "지역": random.choice(REGIONS),
                "카테고리": category,
                "제품": product,
                "판매수량": units,
                "단가": unit_price,
                "매출": units * unit_price,
                "담당자": random.choice(REPS),
            }
        )
    rows.sort(key=lambda r: r["날짜"])

    out = Path(__file__).parent / "dummy_sales.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)}건 트랜잭션 -> {out}")
    return out


if __name__ == "__main__":
    main()
