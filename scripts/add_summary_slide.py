#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TypedDict


ROOT: Final = Path(__file__).resolve().parents[1]
MANIFEST_PATH: Final = ROOT / "summaries" / "manifest.json"
SUMMARY_INDEX_PATH: Final = ROOT / "summary-index.html"
TEMPLATE_PATH: Final = ROOT / "templates" / "summary-slide-template.html"


class SummaryRecord(TypedDict):
    unit: str
    order: str
    title: str
    subtitle: str
    pages: str
    href: str
    updated: str


@dataclass(frozen=True, slots=True)
class SlideRequest:
    unit: str
    order: str
    title: str
    subtitle: str
    pages: str
    href: str
    updated: str
    source_html: Path | None
    scaffold: bool


def load_manifest() -> list[SummaryRecord]:
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(records: list[SummaryRecord]) -> None:
    records.sort(key=lambda item: (item["order"], item["unit"], item["title"]))
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert_record(records: list[SummaryRecord], request: SlideRequest) -> list[SummaryRecord]:
    record: SummaryRecord = {
        "unit": request.unit,
        "order": request.order,
        "title": request.title,
        "subtitle": request.subtitle,
        "pages": request.pages,
        "href": request.href,
        "updated": request.updated,
    }
    return [item for item in records if item["href"] != request.href] + [record]


def scaffold_html(request: SlideRequest) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    concepts = "".join(
        f"<div class=\"tile\"><strong>{label}</strong>{body}</div>"
        for label, body in [
            ("개념 1", "여기에 쉬운 설명을 적습니다."),
            ("개념 2", "교과서 예시와 생활 속 비유를 연결합니다."),
        ]
    )
    replacements = {
        "{{UNIT}}": html.escape(request.unit),
        "{{TITLE}}": html.escape(request.title),
        "{{SUMMARY}}": html.escape(request.subtitle),
        "{{CONCEPT_TILES}}": concepts,
        "{{KEY_SENTENCE}}": "한 줄 정리를 여기에 적습니다.",
        "{{QUIZ_PROMPT}}": "정리한 개념을 확인하는 객관식 문제를 여기에 적습니다.",
        "{{QUIZ_ANSWER}}": "정답과 해설을 여기에 적습니다.",
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def write_slide_file(request: SlideRequest) -> None:
    target = ROOT / request.href
    target.parent.mkdir(parents=True, exist_ok=True)
    if request.source_html is not None:
        shutil.copyfile(request.source_html, target)
        return
    if request.scaffold:
        target.write_text(scaffold_html(request), encoding="utf-8")


def render_summary_index(records: list[SummaryRecord]) -> str:
    cards = "\n".join(
        f'''<a class="summary-card" href="{html.escape(item["href"], quote=True)}">
          <span>{html.escape(item["order"])}</span>
          <strong>{html.escape(item["title"])}</strong>
          <small>{html.escape(item["unit"])} · {html.escape(item["pages"])} · {html.escape(item["subtitle"])}</small>
        </a>'''
        for item in records
    )
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>인공지능 기초 정리본</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%232563eb'/%3E%3Cpath d='M18 40h28v6H18zM18 18h28v6H18zM18 29h20v6H18z' fill='white'/%3E%3C/svg%3E">
  <style>
    :root {{ --bg:#f5f7fb; --card:#ffffff; --ink:#172033; --muted:#667085; --line:#d9e0ec; --accent:#2563eb; --soft:#eef4ff; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; background:linear-gradient(180deg,#eaf2ff 0%,var(--bg) 360px); color:var(--ink); font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; line-height:1.55; }}
    main {{ width:min(1120px,calc(100% - 32px)); margin:42px auto 64px; }} .hero {{ background:rgba(255,255,255,.82); border:1px solid var(--line); border-radius:28px; padding:32px; box-shadow:0 24px 70px rgba(31,41,55,.12); }}
    .eyebrow {{ margin:0 0 8px; color:var(--accent); font-weight:800; }} h1 {{ margin:0; font-size:clamp(2rem,5vw,3.5rem); letter-spacing:-.055em; line-height:1.05; }} .lead {{ max-width:760px; margin:16px 0 0; color:var(--muted); font-size:1.05rem; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; margin-top:28px; }} .summary-card {{ display:grid; grid-template-columns:auto 1fr; gap:4px 12px; align-items:center; min-height:104px; padding:16px; border:1px solid var(--line); border-radius:18px; background:var(--card); color:var(--ink); text-decoration:none; box-shadow:0 10px 28px rgba(31,41,55,.06); }}
    .summary-card:hover {{ border-color:#93c5fd; box-shadow:0 16px 34px rgba(37,99,235,.13); transform:translateY(-2px); }} .summary-card span {{ grid-row:1 / span 2; display:grid; place-items:center; width:44px; height:44px; border-radius:14px; background:#dbeafe; color:#1d4ed8; font-weight:900; }} small {{ color:var(--muted); }} .back {{ display:inline-block; margin-top:18px; color:#1d4ed8; font-weight:800; text-decoration:none; }}
    @media (max-width:760px) {{ main {{ margin-top:20px; }} .hero {{ padding:22px; border-radius:22px; }} .grid {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body><main><section class="hero"><p class="eyebrow">대성여자고등학교 · 인공지능 기초</p><h1>쉬운 설명 정리본</h1><p class="lead">어려운 개념을 슬라이드 형식으로 정리한 HTML만 모아 둔 페이지입니다.</p><a class="back" href="index.html">질문폼 목록으로 돌아가기</a></section><section class="grid">{cards}</section></main></body></html>
'''


def write_summary_index(records: list[SummaryRecord]) -> None:
    SUMMARY_INDEX_PATH.write_text(render_summary_index(records), encoding="utf-8")


def parse_args() -> SlideRequest:
    parser = argparse.ArgumentParser(description="Register a summary slide and refresh summary-index.html")
    parser.add_argument("--unit", required=True)
    parser.add_argument("--order", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--pages", required=True)
    parser.add_argument("--href", required=True)
    parser.add_argument("--updated", required=True)
    parser.add_argument("--source-html", type=Path)
    parser.add_argument("--scaffold", action="store_true")
    args = parser.parse_args()
    return SlideRequest(args.unit, args.order, args.title, args.subtitle, args.pages, args.href, args.updated, args.source_html, args.scaffold)


def main() -> None:
    request = parse_args()
    write_slide_file(request)
    records = upsert_record(load_manifest(), request)
    save_manifest(records)
    write_summary_index(records)


if __name__ == "__main__":
    main()
