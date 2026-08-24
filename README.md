# 인공지능 기초 생기부 질문폼

코들 코스웨어와 강의용 PPT 수업 후 사용하는 소단원별 질문폼입니다.

- 메인: `index.html`
- 질문폼: `forms/*.html`
- 쉬운 설명 정리본 목록: `summary-index.html`
- 정리본 등록 자동화: `scripts/add_summary_slide.py`
- 반: 인공지능C, 인공지능F, 인공지능G
- 수집: Google Apps Script를 통해 스프레드시트 `응답` 시트로 전송

학생 개인정보가 입력되는 응답 스프레드시트는 담당 교사만 접근하도록 관리합니다.

## 쉬운 설명 정리본 추가

어려운 개념을 슬라이드형 HTML로 정리한 뒤 아래 명령으로 등록하면, `summary-index.html`이 자동 갱신됩니다.

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

빈 슬라이드 템플릿부터 시작하려면 `--source-html` 대신 `--scaffold`를 사용합니다. 자세한 절차는 `docs/summary-slide-workflow.md`를 참고합니다.
