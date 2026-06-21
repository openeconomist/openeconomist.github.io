import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = "draft/OpenEcon_Beamer_v3.pdf"


class ElementCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class PresentationPdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = ElementCollector()
        cls.parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        cls.elements = cls.parser.elements

    def test_pdf_asset_exists(self):
        self.assertTrue((ROOT / PDF_PATH).is_file())

    def test_page_links_to_presentation_section(self):
        links = [attrs for tag, attrs in self.elements if tag == "a"]
        self.assertTrue(any(link.get("href") == "#presentation" for link in links))

    def test_page_has_pdf_embed(self):
        embeds = [
            attrs
            for tag, attrs in self.elements
            if tag in {"iframe", "object"}
        ]
        self.assertTrue(
            any(
                embed.get("src") == PDF_PATH or embed.get("data") == PDF_PATH
                for embed in embeds
            )
        )

    def test_page_has_new_tab_pdf_link(self):
        links = [attrs for tag, attrs in self.elements if tag == "a"]
        self.assertTrue(
            any(
                link.get("href") == PDF_PATH and link.get("target") == "_blank"
                for link in links
            )
        )

    def test_page_has_download_links(self):
        links = [attrs for tag, attrs in self.elements if tag == "a"]
        downloads = [
            link
            for link in links
            if link.get("href") == PDF_PATH and "download" in link
        ]
        self.assertGreaterEqual(len(downloads), 2)

    def test_presentation_styles_include_responsive_viewer(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn(".presentation-viewer", css)
        self.assertIn("@media (max-width: 820px)", css)


if __name__ == "__main__":
    unittest.main()
