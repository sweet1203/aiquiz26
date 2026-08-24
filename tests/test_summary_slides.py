import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SummarySlideWorkflowTest(unittest.TestCase):
    def test_manifest_includes_existing_info_search_slide(self) -> None:
        data = json.loads((ROOT / "summaries" / "manifest.json").read_text(encoding="utf-8"))
        hrefs = {item["href"] for item in data}
        self.assertIn("forms/ai-04-1-2-1-info-search-slides.html", hrefs)

    def test_summary_index_links_only_registered_slides(self) -> None:
        data = json.loads((ROOT / "summaries" / "manifest.json").read_text(encoding="utf-8"))
        index = (ROOT / "summary-index.html").read_text(encoding="utf-8")
        for item in data:
            self.assertIn(item["href"], index)
        self.assertNotIn("forms/ai-04-1-2-1.html", index)

    def test_summary_workflow_docs_include_scaffold_command(self) -> None:
        docs = (ROOT / "docs" / "summary-slide-workflow.md").read_text(encoding="utf-8")
        self.assertIn("--scaffold", docs)
        self.assertIn("scripts/add_summary_slide.py", docs)


if __name__ == "__main__":
    unittest.main()
