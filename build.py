#!/usr/bin/env python3
"""
Build jrleja.github.io from content/ + templates/ into a single static page.

    python3 build.py                    # -> preview.html  (safe: not the live page)
    python3 build.py --out index.html   # -> the published page
    python3 -m http.server 8000         # then open localhost:8000/preview.html

Content model
-------------
content/site.yml          site-wide settings and the section order (see `sections:`)
content/<name>.md         a prose section: YAML front matter + Markdown body
content/group/*.md        one file per person
content/research/*.md     one file per research direction
content/<name>.yml        a structured list (press, talks, publications)

Nothing about the site's content is hard-coded in this file. To add a group member,
drop a new .md into content/group/. To reorder anything, edit `order:` in its front
matter. To add or remove a whole section, edit `sections:` in content/site.yml.

Requires: jinja2, markdown, pyyaml (all already installed on this machine).
"""

import argparse
import pathlib
import sys

try:
    import jinja2
    import markdown
    import yaml
except ImportError as exc:  # pragma: no cover - dependency guidance
    sys.exit(f"missing dependency: {exc.name}\n  pip3 install jinja2 markdown pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"

# Markdown extensions: smart typography, and tables for the alumni list.
MD = markdown.Markdown(extensions=["smarty", "tables", "attr_list"])


def render_markdown(text):
    """Markdown -> HTML. Reset between calls so state can't leak."""
    MD.reset()
    return MD.convert(text.strip())


def render_inline(html):
    """Strip the wrapping <p> from a single-paragraph render.

    Short blurbs get interpolated into headings and list items, where a block-level
    <p> would be invalid. Multi-paragraph bodies are returned untouched.
    """
    if html.startswith("<p>") and html.endswith("</p>") and "<p>" not in html[3:]:
        return html[3:-4]
    return html


def split_front_matter(path):
    """Return (metadata, body) for a Markdown file with optional YAML front matter.

    Front matter is delimited by lines of exactly '---'. A file with no front
    matter is treated as all body, which keeps simple prose files simple.
    """
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("\n---", 2)
    if len(parts) < 2:
        raise ValueError(f"{path.name}: front matter opened with --- but never closed")
    meta = yaml.safe_load(parts[0].lstrip("-\n")) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"{path.name}: front matter must be a YAML mapping")
    return meta, parts[1]


def load_page(name):
    """Load a single prose file, e.g. 'intro.md', as a dict with rendered HTML."""
    path = CONTENT / name
    if not path.exists():
        raise FileNotFoundError(f"content/{name} is referenced by site.yml but missing")
    meta, body = split_front_matter(path)
    return {**meta, "html": render_markdown(body), "source": name}


def load_collection(dirname):
    """Load every .md in content/<dirname>/, sorted by `order:` then filename.

    Items without an explicit `order:` sort to the end rather than crashing, so a
    hastily-added file still builds.
    """
    directory = CONTENT / dirname
    if not directory.is_dir():
        raise FileNotFoundError(f"content/{dirname}/ is referenced by site.yml but missing")
    items = []
    for path in sorted(directory.glob("*.md")):
        meta, body = split_front_matter(path)
        html = render_markdown(body)
        items.append(
            {**meta, "html": html, "inline": render_inline(html), "source": path.name}
        )
    items.sort(key=lambda d: (d.get("order", 10**6), d["source"]))
    return items


def load_data(name):
    """Load a structured YAML list, e.g. 'press.yml'.

    Any `body:` field on an entry is treated as Markdown so prose can carry links.
    """
    path = CONTENT / name
    if not path.exists():
        raise FileNotFoundError(f"content/{name} is referenced by site.yml but missing")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    for entry in data:
        if isinstance(entry, dict) and "body" in entry:
            entry["html"] = render_markdown(entry["body"])
    return data


def build_sections(spec):
    """Turn site.yml's `sections:` list into rendered section dicts.

    Each entry names a template in templates/sections/ and one source. The source
    kind is inferred: a directory name is a collection, a .yml is a data list, a
    .md is prose.

    The list is called `entries`, NOT `items`: in a Jinja template `section.items`
    silently resolves to the dict's built-in .items method instead of the key, and
    the loop then fails with an unhelpful TypeError. Do not rename it back.
    """
    sections = []
    for entry in spec:
        source = entry.get("source")
        section = dict(entry)
        if source is None:
            section["entries"], section["body"] = [], ""
        elif source.endswith(".md"):
            page = load_page(source)
            section.setdefault("title", page.get("title"))
            section["body"] = page["html"]
            section["entries"] = []
        elif source.endswith(".yml"):
            section["entries"] = load_data(source)
            section["body"] = ""
        else:
            section["entries"] = load_collection(source)
            section["body"] = ""
        sections.append(section)
    return sections


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument(
        "--out",
        default="preview.html",
        help="output file (default: preview.html, which is gitignored; "
        "pass --out index.html to write the published page)",
    )
    args = parser.parse_args()

    site = yaml.safe_load((CONTENT / "site.yml").read_text(encoding="utf-8"))
    sections = build_sections(site.pop("sections", []))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES)),
        autoescape=jinja2.select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,  # fail loudly on a typo'd variable
    )
    html = env.get_template("base.html").render(site=site, sections=sections)

    out = ROOT / args.out
    out.write_text(html, encoding="utf-8")
    n_entries = sum(len(s["entries"]) for s in sections)
    print(
        f"wrote {out.relative_to(ROOT)}  "
        f"({len(html):,} bytes, {len(sections)} sections, {n_entries} entries)"
    )


if __name__ == "__main__":
    main()
