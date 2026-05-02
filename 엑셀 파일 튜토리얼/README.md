# 엑셀 파일 튜토리얼

파이썬으로 더미 매출 데이터를 만들고, 미니멀한 스타일의 엑셀 보고서를 생성하는 예제.

## 실행

```bash
pip install pandas openpyxl
python3 generate_data.py    # dummy_sales.csv 생성 (180건, seed=42)
python3 build_report.py     # sales_report.xlsx 생성
```

## 산출물

- `dummy_sales.csv` — 2025년 가상 트랜잭션 180건 (날짜·지역·카테고리·제품·수량·단가·매출·담당자)
- `sales_report.xlsx` — 3개 시트로 구성된 분석 보고서
  - **개요**: 타이틀 · 액센트 바 · 4개 KPI 타일 · 보고서 구성 안내
  - **원본 데이터**: 헤더 고정, 통화/숫자 서식, 짝수 행 밴딩
  - **분석 결과**: 월별 매출(라인 차트) · 지역별 매출(바 차트) · 카테고리별 실적 · Top 5 담당자

## 디자인 원칙

미니멀 · 가독성 우선 · 단일 액센트.

| 용도 | 컬러 | HEX |
|---|---|---|
| 헤드라인 액센트 / 강조 지표 | Red | `#A50034` |
| 본문 텍스트 | Neutral Gray | `#6B6B6B` |
| 라벨 · 보조 라인 | Premium Silver | `#8A8D8F` |
| KPI 강조값 · 섹션 부제 | Highlight Gold | `#85714D` |

추가 규칙
- 시트 격자선 비표시 (`showGridLines = False`)
- 헤더 하단에만 얇은 실버 라인
- 통화는 `"₩"#,##0` 서식, 정수는 `#,##0`
- 텍스트 좌측 / 숫자 우측 정렬
- 한 셀에는 하나의 액센트 컬러만 사용
