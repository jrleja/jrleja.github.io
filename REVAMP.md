# Website Revamp — Working Plan

**How to use this file:** it is the single source of truth across sessions. Open a new
Claude Code session in this repo and say *"read REVAMP.md and do the next session"*.
Everything needed to resume cold is in here. Update the Status block at the end of
every session.

---

## Status

- **Next session:** 9–10 — rewrite Research. **Read `RESEARCH-BRIEF.md` first**: it
  holds the theme breakdown from CV.tex, three candidate framings with a
  recommendation, and the five questions only Joel can answer.
- **Live site:** **the new generated site is LIVE** as of 2026-08-17
- **Last updated:** 2026-08-17

**Session 6 — done.** Metadata and an accessibility pass.

`tools/make-images.py` generates `favicon.svg`, `favicon-32.png`,
`apple-touch-icon.png` and `images/og-card.jpg` (1200×630) — rendered through headless
Chrome so the type matches the site, then downscaled with Pillow, which is sharper than
asking Chrome to draw 32 px text. **Re-run it after changing the avatar or the
palette**; it reads the teal straight out of `site.css`.

Added: canonical URL, full Open Graph + `twitter:card` tags, per-theme `theme-color`,
favicon links. Pasting the URL into Slack or Bluesky now shows a real card.

Accessibility fixes, all found by auditing rather than guessing:

- **Outreach skipped a heading level** (h2 → h4). Feature titles are now `h3`.
- **Research figure captions were `h4`s**, so the document outline read as a list of
  figure titles. They are `<figcaption>` inside `<figure>` now.
- **Landmarks were missing.** `<div id="main">` → `<main>`, the sidebar `<section>` →
  `<header>`, the page `<section id="footer">` → `<footer>`, plus `aria-label` on the
  nav and `aria-labelledby` on each section. Added a **skip-to-content link**, which
  matters here because the sidebar's nav comes first in the DOM.
- The banner had `alt=""`; it now describes the SED figure.
- **Three contrast pairs sat just under AA** and were nudged: dimmed text on the sunken
  footer (4.41 → 4.54), the light sidebar nav (4.31 → 4.69), and the dark sidebar nav
  (4.41 → 5.22). **Every pair in both themes now clears 4.5:1**, worst case 4.54.

The HTML5 UP footer credit is gone, along with the last reference to the old theme.

Verified: no heading-level skips, every `<img>` has meaningful alt text, all landmarks
present, no horizontal overflow at 414/768/1440, HTML well-formed.

**Session 7 — done, out of order. The swap is complete.** `index.html` is now built by
`build.py`, and `build.py` with no arguments writes `index.html` (pass
`--out preview.html` for a scratch build). Published page weight: **1.08 MB**, down from
4.36 MB.

Deleted 28 now-dead files, 4.56 MB: the whole HTML5 UP theme (`main.css`, its `sass/`
sources, Font Awesome CSS and 1 MB of icon webfonts, jQuery and its five plugins), the
superseded `ashtekar.png` and `nikko_cleri.png`, and the four remaining alumni photos.
`assets/` went from 1.3 MB to 24 KB; `images/` from 15 MB to 1.1 MB.

**Lesson worth keeping:** the first pass at finding dead files used
`(?:src|href)["\']?(...)` — missing the `=` — so it matched almost nothing and
confidently listed `avatar.jpg`, `site.js` and `CV.pdf` as unreferenced. Printing the
list before deleting caught it. Never pipe a delete straight from a match.

Also done this session, from Joel's review of the preview:

- `avatar.jpg` and `marta_laska.jpeg` recropped square from the full-resolution
  originals with the face at ~40–45% height. Both were tall portraits, so the CSS
  centre-crop had been cutting the tops of their heads off. A square source means the
  CSS crops nothing.
- Section order is now **intro → press → group → outreach → research → contact**:
  press promoted, research demoted pending its rewrite.
- `(firstname).(lastname)@psu.edu` → a plain `mailto:` link.

### Remaining sessions

6 (metadata: favicon + OG card), 9–10 (rewrite Research), 11 (Talks & Media),
12 (press refresh), 13 (selected publications), 14 (join the group), 15–16 (link check,
final pass). Sessions 5 and 8 are complete.

Still open: **B5** — the Feb 2024 press item's PopSci link was wrong (it pointed at the
Nov 2023 story) and was dropped rather than guessed; Session 12 should find the real
one. And the footer still credits HTML5 UP, whose code is now entirely gone — kept as an
honest nod to the layout's lineage, but fine to drop from `templates/base.html`.

**Session 5 — done.** Page weight **4.36 MB → 1.11 MB (74% smaller)**.

| file | before | after |
|---|---|---|
| `avatar.jpg` | 8317 KB (3459×5188!) | 61 KB (400×600) |
| `ashtekar.png` → `.jpg` | 1803 KB | 61 KB |
| `animation.gif` | 964 KB | 311 KB (760 px, 256 colours, 8 frames kept) |
| `allyson_garcia.png` → `.jpg` | 763 KB | 37 KB |
| `nikko_cleri.png` → `.jpg` | 566 KB | 29 KB |
| `6points.jpg` | 410 KB | 67 KB |
| `marta_laska.jpeg` | 378 KB | 38 KB |
| `fsf.jpg` | 291 KB | 79 KB |
| `banner.jpg` | 80 KB | 27 KB |

Deleted outright: `old_avatar.jpg`, `read-only.zip` (1007 KB of template cruft),
`kanishk_pandey.jpeg`, `nathan_cristello.jpeg` (unreferenced since alumni became a text
list). `placeholder-person.svg` stays — it is the template's fallback for anyone with
no `photo:`.

Two things worth knowing. Re-encoding is **only kept when it actually shrinks the
file** — `emilie_burnham_faith.jpeg` grew from 20 KB to 44 KB on the first pass because
it was already well compressed, and had to be restored. And `animation.gif` could drop
a further 175 KB as an mp4 (134 KB), but that needs a `<video>` tag and raises
autoplay/reduced-motion questions; not worth it for a figure Sessions 9–10 may replace.

Originals are backed up in the session scratchpad, and git history has them regardless.

### Still to delete at the Session 7 swap

Only the live `index.html` still references these:

- `images/ashtekar.png` (1803 KB), `images/nikko_cleri.png` (566 KB)
- `images/william_bowman.jpeg` (951 KB), `bingjie_wang.jpeg`, `yijia_li.jpeg`,
  `Junyu Zhang.jpeg` — alumni photos
- `assets/css/main.css`, `assets/css/font-awesome.min.css`, `assets/fonts/`,
  `assets/js/jquery*` and the other old scripts (~1250 KB)

Reclaimable: **~3.3 MB of images + ~1.25 MB of old assets.**

**Session 4 — done.** `assets/css/site.css` replaces the 2018 template. The layout
that defines the site is preserved (fixed teal sidebar on the right, content left), but
everything under it is new: CSS-grid, custom-property tokens, dark mode, and a system
font stack.

| | before | after |
|---|---|---|
| CSS | 53.5 KB + 30.3 KB Font Awesome | 11.5 KB |
| Webfonts | 1060 KB of icon fonts | 0 — two inline SVGs |
| JS | 107.7 KB (jQuery + 5 plugins) | 1.9 KB vanilla |
| External requests | Google Fonts (render-blocking) | none |
| **Total** | **1251.7 KB** | **13.3 KB** |

Smooth scrolling is now `scroll-behavior`, the mobile nav is CSS (the sidebar just
stacks), and the only thing that still needs JS is highlighting the nav link for the
section in view — an IntersectionObserver in `assets/js/site.js`.

**A real accessibility bug is fixed.** The old teal `#4acaa8` gave white text just
**2.04:1** contrast, well under the WCAG AA floor of 4.5:1 — that failure is on the
live site today. The sidebar is now `#1d7a63` (5.23:1) and link text `#1a7a62`
(5.24:1). Same hue, and both are single tokens at the top of `site.css`.

Verified with headless Chrome: no horizontal overflow at 360/414/768/1024/1440 px, the
people grid goes 2→3 columns, and the page validates as well-formed HTML. Caution when
screenshotting — **headless Chrome clamps its viewport to a 500 px minimum**, so a
narrower `--window-size` silently clips rather than reflows. Measure `scrollWidth`
instead of trusting the picture.

Two bugs found by actually looking at the render: the research figure-caption style was
leaking into the Outreach headings (both used `article > .inner > h4`; research figures
now carry a `.figure` class), and the press date's trailing colon detached from its
fixed-width label column.

The old `main.css`, Font Awesome, webfonts and jQuery **stay in the repo for now** —
the live `index.html` still loads them. They get deleted at the Session 7 swap.

**Session 3 — done.** All content is now data. Six sections build from `content/`:
Intro, Leja Group, Research, Press, Outreach, Contact. `preview.html` validates as
well-formed HTML; the live `index.html` has six structural errors (unclosed `<li>`s in
the press list, an unclosed `<p>` in Research) that the port fixes for free.

Deliberate changes from the live page, all reversible:

- **Press is its own nav section** instead of a bullet list buried at the end of Intro.
- **Alumni are a text list**, grouped into grads/postdocs and undergrads, expanded from
  4 people to the full 17 from CV.tex.
- **Session 8 is now mostly done**: all 9 current members are in, with the five new
  photos. What remains is the three TODO blurbs below.
- Typos fixed: "persepctive" → "perspective", "In additional to" → "In addition to".
- The 2019 figure now links the published paper (`2019ApJ...877..140L`) rather than the
  superseded arXiv preprint.
- **Needs your approval:** the sidebar ADS link now points at your curated public
  library (`G3CNFVQISayWjz8Fz-9n5g`, the one your CV calls the complete list) instead of
  an author-name search. Revert in `content/site.yml` if you prefer the search.

`build.py` gained three things: a section can draw on several sources via `sources:`;
`caption:` fields render Markdown; and the build **refuses to write `index.html` while
any TODO placeholder remains**, so Session 7 cannot ship filler.

### Blocked on you — three blurbs

`content/group/lishan-shi.md`, `connor-luettgenau.md` and `allyson-garcia.md` each
contain a one-line `TODO:`. I don't know what these three work on and won't invent it.
One sentence each, in the style of the others, and Session 8 closes.

**Session 2 — done.** `build.py` + `templates/` + `content/site.yml` exist and build
green. Intro and Contact are ported and wired; the group / research / press / talks /
pubs templates are written and smoke-tested but not yet wired into `site.yml` — that's
Session 3, which is now pure content work.

Output goes to **`preview.html`** (gitignored) until Session 7, so the live
`index.html` cannot be touched by accident. Two gotchas found and fixed, both worth
knowing before editing templates:

- The section list is `section.entries`, **never** `section.items` — Jinja resolves
  `.items` to the dict method and fails with an unhelpful `TypeError`.
- Content files carry **plain text, never HTML entities**. Templates escape on output,
  so `&` is correct and `&amp;` renders as `&amp;amp;`.

Optional front-matter fields are read with `.get()` because the build runs with
`StrictUndefined` (which catches typos in `site.yml` but raises on any missing key).

**Session 1 — done.** Fixed B2 (the broken `</h4>`) and B3 (Early → Mid-Career), and
refreshed `files/CV.pdf` to the May 2026 version. Added `.gitignore` and a reusable
`images/placeholder-person.svg` for the people who still need photos (Session 8).
Still open from Phase 0: **B5** and **B6** (press-link sloppiness) — fixed when press
moves into `content/press.yml` in Session 12.

### ⚠️ Read this before working in this clone again

**This local clone was orphaned.** It forked from the real repo on 2023-11-14 (local
`e49f753` vs remote `18e7caf` — the same update, committed twice) and then sat unaware
of ten subsequent commits. Since then the site has been published from **the GitHub
web UI** (hence the `Add files via upload` commits), so the *live site was never
stale* — this laptop's copy was.

Session 1 initially drew the opposite conclusion from this clone's history and nearly
pushed two regressions: replacing Marta Laska's real photo with a placeholder, and
re-adding a `mentoring_leja_group.pdf` that already exists on the live site. The push
was rejected by the remote, which is the only reason neither landed.

Work now continues on branch `session1-fixes`, based on the true `origin/main`.
**Local `main` still points at the orphaned commit `e49f753` and should be deleted or
reset once this branch is merged.** Always `git fetch && git status` before starting,
and prefer committing from this clone over uploading through the browser.

---

## Why this plan looks the way it does

The constraint is not the work, it's the schedule: ~10–15 minutes, twice a day, for
1–2 weeks. So the plan is a **queue of independently shippable commits**, not a
project. Rules:

1. **The site is never broken.** Every session ends with something committable.
2. **The rebuild happens behind the live site**, not in front of it. New files are
   added alongside; `index.html` is only swapped once the new build matches.
3. **No session depends on remembering the last one.** Each has a written goal and a
   definition of done.

---

## Findings from the audit (2026-08-14)

All verified against the **real** `origin/main`, not the orphaned clone.

### Bugs

| # | Status | Problem |
|---|--------|---------|
| B2 | **fixed in S1** | `index.html:203` — `</h4>` closed mid-sentence, leaking `author --> postdoctoral researcher at Northwestern University.` as stray body text on the live page |
| B3 | **fixed in S1** | Sidebar said "Mid-Career Professor", intro said "Early Career". CV.tex confirms **Mid-Career** (2024–present) |
| B5 | open → S12 | `index.html:71` — Feb 2024 press item has an unclosed `(`, and its "PopSci" link is a copy-paste of the Nov 2023 item's URL |
| B6 | open → S12 | Many `href=` values are unquoted with a stray trailing `//` |
| ~~B1~~ | **not a bug** | `images/marta_laska.jpeg` exists on the live site; it was only missing from the orphaned clone |
| ~~B4~~ | **not a bug** | `files/mentoring_leja_group.pdf` exists on the live site (added Aug 2025) |

### Staleness — all confirmed live

- **Research section stops at 2019** (last heading is `<h4>2019`). Nothing on JWST,
  RUBIES, UNCOVER, little red dots, Prospector-β, simulation-based inference, or PFS —
  i.e. nothing you're currently known for.
- **Press stops at June 2024.** Missing at minimum the 2025 PSU/Max Planck release
  *"Mysterious red dots in early universe may be black hole star atmospheres"*.
- **Group roster is a year behind.** On the site but not in CV.tex order, and
  **entirely missing**: Lishan Shi, Allyson Garcia, Connor Luettgenau, Senti Bo,
  Si Rui, Gautam Nagaraj, Kanishk Pandey, Nathan Cristello.
- **No talks section**, no publications section, no "join the group" section.

### Technical — all confirmed live

- `images/avatar.jpg` is **8.5 MB**; `images/` totals **14 MB**. Brutal on conference
  wifi and phones.
- `user-scalable=no` in the viewport meta blocks pinch-zoom — an accessibility failure.
- **Zero** `og:` tags and no `meta description` → links shared to Slack / Bluesky /
  Twitter show a blank card.
- Font Awesome 4 (2016) + jQuery + the 2018 HTML5 UP "Read Only" template.
- `images/old_avatar.jpg` unused; `read-only.zip` (1 MB) is template cruft.

---

## Architecture

**Generator: a ~120-line Python script.** Content lives in Markdown/YAML; `build.py`
renders it through Jinja2 templates into `index.html`, which is committed.

Why Python rather than Jekyll or Astro — decided from what's actually on this machine:

- `node`/`npm`: **not installed**. Astro needs a Homebrew install plus a GitHub Action.
- `ruby`: system **2.6.10** with Bundler 1.17. Jekyll on macOS system Ruby means rbenv,
  native gem builds, and a toolchain that rots between uses.
- `python3` **3.11.7** with `jinja2`, `markdown`, and `pyyaml` **already present**.

This delivers exactly the thing that was wanted — *adding a student is a new `.md`
file; the site rebuilds itself* — with zero new ecosystem, in the language already in
daily use. Because the built `index.html` is committed, GitHub Pages needs no
configuration and the deploy cannot break. And `python3 build.py` is a command that
will still make sense in eight months.

```
jrleja.github.io/
├── build.py                  # the generator
├── content/
│   ├── site.yml              # name, titles, nav, sidebar links
│   ├── intro.md
│   ├── research/*.md         # one file per research direction
│   ├── group/*.md            # one file per person
│   ├── talks.yml             # invited talks + public lectures + media
│   ├── press.yml             # date, title, outlet, url, coverage[]
│   └── pubs.yml              # selected publications
├── templates/
│   ├── base.html
│   └── sections/*.html
├── assets/css/site.css       # new, hand-written, no jQuery
├── images/                   # optimized
├── files/                    # CV.pdf, mentoring_leja_group.pdf
├── index.html                # BUILT OUTPUT — committed, served by GitHub Pages
└── REVAMP.md                 # this file
```

---

## The sessions

Each is sized for **10–15 minutes**. Ship a commit at the end of every one.

### Phase 1 — Scaffold

**Session 2 · Write `build.py` + templates** ⏱ 15 min
Generator, `base.html`, section templates, `content/site.yml`. Nothing user-visible.
*Done when:* `python3 build.py` runs and emits a valid `index.html`.

**Session 3 · Port existing content into `content/`** ⏱ 15 min
Move today's intro, research, group, outreach, press into Markdown/YAML.
*Done when:* the built page is visually equivalent to the current site. **Now the
content is data and every later session is just editing text.**

### Phase 2 — Design

**Session 4 · New stylesheet** ⏱ 15 min
Typography, CSS-grid layout, dark mode, responsive. Drop jQuery and Font Awesome 4.

**Session 5 · Images** ⏱ 10 min
8.5 MB avatar → ~150 KB. Resize/compress all of `images/` (14 MB → ~1.5 MB). Delete
`old_avatar.jpg` and `read-only.zip`.

**Session 6 · Metadata + accessibility** ⏱ 10 min
Favicon, `meta description`, Open Graph / Twitter card image, remove
`user-scalable=no`, alt text, heading order, contrast.
*Done when:* pasting the URL into Slack shows a real preview card.

### Phase 3 — Content (the actual point)

**Session 7 · Swap `index.html` to the new build** ⏱ 10 min
The only risky moment. Preview locally first (`python3 -m http.server`), then push.

**Session 8 · Group roster** ⏱ 15 min
From CV.tex. Add **Lishan Shi** (Statistics grad, 2025–), **Allyson Garcia** (2026–),
**Connor Luettgenau** (2025–), **Senti Bo** and **Si Rui** (Nanjing, 2025). Add
**Kanishk Pandey** (2023–2024), **Nathan Cristello** (2023–2024) and **Gautam Nagaraj**
(→ EPFL) to Former. Add outcomes to every alum.
*Needs from you:* photos for the new people (`placeholder-person.svg` in the meantime).

**Sessions 9–10 · Rewrite Research** ⏱ 15 min each — *the biggest lift*
Replace the 2013–2019 thesis narrative. Proposed arc: (1) the SED-fitting problem and
Prospector; (2) JWST and the early universe — little red dots, UNCOVER, RUBIES;
(3) machine learning and simulation-based inference; (4) PFS and what's next.
I draft from CV + papers; you correct the framing.

**Session 11 · Talks & Media** ⏱ 15 min
Griffith Observatory, Ashtekar lecture, IAU Commission J1 (2026), CMU SBI keynote
(2025), STScI/JHU colloquium, the NHK documentary, podcast/video interviews.
*Needs from you:* the Griffith link/date and any interviews not in the CV.

**Session 12 · Press refresh** ⏱ 15 min
Add the 2025 black-hole-star release; fill 2024–2026 gaps via web search; fix B5 and
B6; verify every existing link still resolves.

**Session 13 · Selected publications** ⏱ 10 min
~12 papers with links, from CV.tex first/second/third-author lists, plus the ADS
library link (`G3CNFVQISayWjz8Fz-9n5g`).

**Session 14 · Join the group** ⏱ 10 min
What you look for, how to apply, prospective-student framing. Link the existing
`files/mentoring_leja_group.pdf` directly rather than through GitHub's PDF viewer.

### Phase 4 — Land it

**Session 15 · Link check + repo hygiene** ⏱ 10 min
Run a link checker over the whole site; fix what's dead. Delete the orphaned local
`main` branch.

**Session 16 · Final pass** ⏱ 15 min
Mobile and cross-browser check, Lighthouse, proofread, push.

---

## Things only you can supply

Collect these whenever they occur to you — drop them in `content/INBOX.md` and I'll
file them.

- [ ] Photos for **Lishan Shi**, **Allyson Garcia**, **Connor Luettgenau**
- [ ] **Griffith Observatory** talk — date, title, link, recording?
- [ ] Recent **interviews / podcasts** not listed in CV.tex
- [ ] How you want **Research** framed — what you most want to be known for now
- [ ] Anything to *remove* (Flipped Science Fair ended 2020 — keep or retire?)

---

## Commands

```sh
git fetch && git status           # ALWAYS do this first
python3 build.py                  # rebuild index.html
python3 -m http.server 8000       # preview at localhost:8000
```
