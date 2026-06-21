# Presentation PDF Website Integration

## Goal

Make `draft/OpenEcon_Beamer_v3.pdf` available from the TaDaS project website
for both in-browser reading and direct download.

## User Experience

- Add a `Presentation` link to the primary navigation.
- Add `View presentation` and `Download PDF` actions to the hero.
- `View presentation` scrolls to a dedicated presentation section on the page.
- `Download PDF` points directly to the PDF and uses the HTML `download`
  attribute.
- The presentation section embeds the PDF at a readable desktop height.
- The section also contains explicit `Open in new tab` and `Download PDF`
  links so the document remains accessible when a browser does not support
  embedded PDF rendering.
- On narrow screens, the viewer height is reduced while the action links wrap
  without overflowing.

## Architecture

Keep the existing dependency-free GitHub Pages architecture:

- Serve the existing PDF as a static repository asset.
- Use native HTML embedding rather than adding a JavaScript PDF library.
- Add only the markup and CSS needed for the navigation item, hero actions,
  presentation section, responsive viewer, and fallback links.

## Accessibility and Failure Handling

- Give the embedded document a descriptive title.
- Preserve visible text links for opening and downloading the PDF.
- Open the standalone viewer in a new tab with safe `rel` attributes.
- Include fallback content inside the embed container for unsupported browsers.

## Verification

- Confirm the PDF path returns the document through a local static server.
- Confirm the hero view link targets the presentation section.
- Confirm every download link targets `draft/OpenEcon_Beamer_v3.pdf` and has a
  `download` attribute.
- Confirm the embedded viewer uses the same PDF path.
- Check the page at desktop and mobile widths for overflow and readable layout.
