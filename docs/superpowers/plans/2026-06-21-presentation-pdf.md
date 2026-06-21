# Presentation PDF Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add native in-page viewing and direct downloading of the existing TaDaS presentation PDF.

**Architecture:** Extend the existing single-page HTML with navigation and hero entry points plus a dedicated native PDF embed. Add focused responsive CSS and validate the static contract with Python standard-library tests and a local HTTP server.

**Tech Stack:** HTML5, CSS, Python `unittest`, Python `http.server`

---

## File Structure

- Modify `index.html`: navigation, hero actions, and the presentation section.
- Modify `styles.css`: presentation layout, embedded viewer, and mobile sizing.
- Create `tests/test_presentation_pdf.py`: static HTML/CSS contract tests for view and download behavior.

### Task 1: Add Static Contract Tests

**Files:**
- Create: `tests/test_presentation_pdf.py`

- [ ] **Step 1: Write the failing tests**

Create tests that parse `index.html` and assert:

```python
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
        embeds = [attrs for tag, attrs in self.elements if tag in {"iframe", "object"}]
        self.assertTrue(any(embed.get("src") == PDF_PATH or embed.get("data") == PDF_PATH for embed in embeds))

    def test_page_has_new_tab_pdf_link(self):
        links = [attrs for tag, attrs in self.elements if tag == "a"]
        self.assertTrue(any(link.get("href") == PDF_PATH and link.get("target") == "_blank" for link in links))

    def test_page_has_download_links(self):
        links = [attrs for tag, attrs in self.elements if tag == "a"]
        downloads = [link for link in links if link.get("href") == PDF_PATH and "download" in link]
        self.assertGreaterEqual(len(downloads), 2)

    def test_presentation_styles_include_responsive_viewer(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn(".presentation-viewer", css)
        self.assertIn("@media (max-width: 820px)", css)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests/test_presentation_pdf.py -v`

Expected: the asset test passes; presentation link, embed, download-link, and CSS tests fail.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_presentation_pdf.py
git commit -m "test: define presentation PDF website contract"
```

### Task 2: Add Presentation Markup

**Files:**
- Modify: `index.html:16-21`
- Modify: `index.html:34-37`
- Modify: `index.html:164-165`

- [ ] **Step 1: Add the navigation and hero actions**

Add a `Presentation` navigation link targeting `#presentation`. In the hero actions, retain the method link and add:

```html
<a class="button secondary" href="#presentation">View presentation</a>
<a class="button text-button" href="draft/OpenEcon_Beamer_v3.pdf" download>Download PDF</a>
```

- [ ] **Step 2: Add the presentation section before the finding section**

```html
<section id="presentation" class="section presentation">
  <div class="presentation-heading">
    <div>
      <p class="eyebrow">Presentation</p>
      <h2>Explore the project slides</h2>
      <p>Read the current TaDaS presentation in your browser or save a copy for later.</p>
    </div>
    <div class="presentation-actions" aria-label="Presentation file actions">
      <a class="button secondary" href="draft/OpenEcon_Beamer_v3.pdf" target="_blank" rel="noopener noreferrer">Open in new tab</a>
      <a class="button primary" href="draft/OpenEcon_Beamer_v3.pdf" download>Download PDF</a>
    </div>
  </div>
  <object
    class="presentation-viewer"
    data="draft/OpenEcon_Beamer_v3.pdf"
    type="application/pdf"
    aria-label="TaDaS project presentation"
  >
    <p>
      This browser cannot display the PDF inline.
      <a href="draft/OpenEcon_Beamer_v3.pdf" target="_blank" rel="noopener noreferrer">Open the presentation in a new tab</a>.
    </p>
  </object>
</section>
```

- [ ] **Step 3: Run the contract tests**

Run: `python -m unittest tests/test_presentation_pdf.py -v`

Expected: all markup tests pass; the CSS viewer test still fails.

### Task 3: Add Responsive Presentation Styling

**Files:**
- Modify: `styles.css:317`
- Modify: `styles.css:359-415`
- Modify: `styles.css:417-436`

- [ ] **Step 1: Add desktop presentation styles before `.finding`**

```css
.presentation {
  border-top: 1px solid var(--line);
}

.presentation-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.presentation-heading p:last-child {
  max-width: 660px;
  margin-bottom: 0;
  color: var(--muted);
}

.presentation-actions {
  display: flex;
  flex-wrap: wrap;
  flex: 0 0 auto;
  gap: 10px;
}

.presentation-viewer {
  display: block;
  width: 100%;
  height: min(78vh, 860px);
  min-height: 620px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  box-shadow: var(--shadow);
}

.text-button {
  border-color: transparent;
  color: var(--accent-dark);
}
```

- [ ] **Step 2: Add mobile layout rules inside the existing 820px media query**

```css
.presentation-heading {
  align-items: flex-start;
  flex-direction: column;
}

.presentation-viewer {
  height: 68vh;
  min-height: 480px;
}
```

- [ ] **Step 3: Include presentation actions in the existing 460px stacked action rules**

Apply the existing column and full-width button treatment to `.presentation-actions` as well as `.actions`.

- [ ] **Step 4: Run all contract tests**

Run: `python -m unittest discover -s tests -v`

Expected: six tests pass.

### Task 4: Browser and HTTP Verification

**Files:**
- Verify: `index.html`
- Verify: `styles.css`
- Verify: `draft/OpenEcon_Beamer_v3.pdf`

- [ ] **Step 1: Start a local static server**

Run: `python -m http.server 8000`

Expected: server listens on port 8000 from the repository root.

- [ ] **Step 2: Verify HTTP responses**

Run:

```bash
curl -I http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/draft/OpenEcon_Beamer_v3.pdf
```

Expected: both return `HTTP/1.0 200 OK`; the PDF returns `Content-type: application/pdf`.

- [ ] **Step 3: Check desktop and mobile rendering**

Open the page at 1440×900 and 390×844. Confirm the presentation section is readable, the PDF viewer remains within the viewport, all buttons are visible, and the narrow layout has no horizontal overflow.

- [ ] **Step 4: Run final automated checks**

Run:

```bash
python -m unittest discover -s tests -v
git diff --check
```

Expected: all tests pass and `git diff --check` prints no errors.

- [ ] **Step 5: Commit the feature**

```bash
git add index.html styles.css tests/test_presentation_pdf.py draft/OpenEcon_Beamer_v3.pdf
git commit -m "Add online presentation viewer and download"
```
