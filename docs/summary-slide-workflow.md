# 쉬운 설명 정리본 HTML 작업 흐름

어려운 개념이 나올 때마다 `forms/*-slides.html` 형식의 슬라이드 정리본을 만들고, `summary-index.html`에 자동 등록합니다.

## 새 정리본을 만들 때

1. 단원, 제목, 쪽수, 핵심 개념을 정합니다.
2. 기존 정리본처럼 쉬운 설명, 비유, 오해 주의, 객관식 답 확인을 포함한 HTML을 만듭니다.
3. 아래 명령으로 HTML을 `forms/`에 복사하고 정리본 목록을 갱신합니다.

```bash
python3 scripts/add_summary_slide.py \
  --unit "1-2-1-1" \
  --order "04" \
  --title "정보이용 탐색 알고리즘" \
  --subtitle "언덕 등반, 최상 우선, A*를 쉬운 설명으로 정리" \
  --pages "36~41쪽" \
  --href "forms/ai-04-1-2-1-info-search-slides.html" \
  --updated "2026-08-24" \
  --source-html "/path/to/정리본.html"
```

## 빈 템플릿부터 시작할 때

```bash
python3 scripts/add_summary_slide.py \
  --unit "2-2-1" \
  --order "15" \
  --title "퍼셉트론과 딥러닝" \
  --subtitle "퍼셉트론, 은닉층, 활성화 함수를 쉬운 설명으로 정리" \
  --pages "90~95쪽" \
  --href "forms/ai-15-2-2-1-deep-learning-slides.html" \
  --updated "2026-08-24" \
  --scaffold
```

생성된 HTML의 placeholder 문장을 실제 수업 내용으로 바꾼 뒤 브라우저에서 확인합니다.

## 업로드 전 확인

```bash
python3 -m html.parser summary-index.html
python3 -m html.parser forms/ai-04-1-2-1-info-search-slides.html
```

브라우저에서 `summary-index.html`을 열어 정리본 링크가 연결되는지 확인합니다.

## 정리본 작성 체크리스트

- 한 번에 한 슬라이드만 보이게 구성합니다.
- 어려운 용어는 생활 속 비유로 다시 설명합니다.
- “오해 주의” 또는 “핵심 구분”을 넣습니다.
- 마지막에는 제출 버튼 없는 객관식 문제와 `답 확인`을 넣습니다.
- 평가 함수처럼 상황에 따라 기준이 달라지는 개념은 “큰 값이 유리한 경우 / 작은 값이 유리한 경우”를 함께 설명합니다.
