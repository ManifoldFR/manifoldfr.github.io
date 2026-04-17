# CLAUDE.md — Site Notes

## Pending Task: Migrate from Terminimal to a Modern Zola Theme

### Goal
Replace the [terminimal](https://github.com/pawroman/zola-theme-terminimal) theme (dated retro terminal aesthetic) with a modern Zola theme, while preserving all existing functionality.

### Chosen Theme: Tabi
[welpo/tabi](https://github.com/welpo/tabi) — most actively maintained modern Zola theme, with built-in KaTeX support (biggest compatibility win).

Alternatives considered:
- **DeepThought** — also has KaTeX, Bulma-based, less active
- **Apollo** — clean/minimal, no built-in KaTeX (needs manual injection)

---

### Key Constraints to Preserve

1. **KaTeX math rendering** (`templates/katex.html`)
   - 160+ math expressions across posts using `$...$`, `$$...$$`, `\(...\)`, `\[...\]`
   - 47 custom macros (`\R`, `\EE`, `\defeq`, `\argmin`, etc.)
   - Must be injected into the new theme's `<head>` via an `extra_head` block (or equivalent)

2. **BibTeX bibliography system** (`templates/bib.html` + `templates/macros.html`)
   - Loads `static/references.bib` via `load_data(format="bibtex")`
   - Custom macros: `process_bib`, `bib_proceedings`, `bib_journal`, `print_ref`
   - These templates can be kept as-is; they extend `index.html`

3. **Profile/bio section on homepage** (`templates/index.html`)
   - Overrides `content` block of the base theme's index
   - Custom HTML: `#subheader` flex layout with profile picture + bio + institution links
   - Styled in `sass/custom.scss`

4. **Tag taxonomy** — must be supported by the new theme

5. **Custom SCSS** (`sass/custom.scss` ~80 lines)
   - `#subheader`, `.profile-picture`, `.address`, `.pub-link`, `.publication`, `.pub-year`, `.pub-journal`, `.my-video`
   - Some colors are crimson (`#9b1919`) — independent of theme accent color

6. **Search index** — `build_search_index = true` in config

---

### Migration Steps

1. Add new theme as a git submodule under `themes/`
2. Set `theme = "<new-theme>"` in `config.toml`
3. Remap `[extra]` config vars — terminimal-specific keys (`accent_color`, `logo_text`, `logo_home_link`, `menu_items`, `favicon`, `page_titles`) need to be replaced with the new theme's schema
4. Find the new theme's head block name (e.g. `extra_head`, `head_extra`) and update `templates/index.html` to inject `katex.html`
5. Adapt the homepage profile section override to the new theme's block structure
6. Verify `templates/bib.html` still extends correctly
7. Port or adapt `sass/custom.scss` (check for naming conflicts with new theme's SCSS)
8. Test: math rendering, publications page, tags, pagination, search

---

### Current Site Structure

- `content/posts/` — blog posts (paginate_by=6, tags)
- `content/publications/_index.md` — template=bib.html
- `content/news/` — transparent section
- `templates/katex.html` — KaTeX CDN + custom macros
- `templates/macros.html` — BibTeX formatting macros
- `templates/bib.html` — publications page
- `templates/index.html` — homepage override (profile section)
- `sass/custom.scss` — site-level styles
- `static/references.bib` — bibliography source
