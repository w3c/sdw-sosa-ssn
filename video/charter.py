"""Style of the SOSA/SSN videos: the W3C/OGC specification page, the notation
of the spec's diagrams (`video/style.md`).

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
    from charter import *          # m, colours, nodes, arrows, cards, Voice…

Two families of objects:

- the page: white background, Noto Sans, headings `#005A9C`, links `#034575`,
  respec `.note` and `.example` boxes;
- the graph: `cls()` a class (white box, solid stroke), `ind()` an
  individual (fill of its category, dotted border, identifier in mono),
  `edge()` a property (solid arrow between classes, dashed between
  individuals), label in italics.

Paths (logos, coastlines) start from the repository root, `REPO`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

import manimgx as m

__all__ = [
    "m", "np", "REPO", "DATA", "INK", "HEADING", "LINK", "LINK_UNDERLINE", "TOC_BG", "ACTIVE", "OGC_BLUE",
    "GREY", "LIGHTGREY", "RULE", "CAT", "FONT", "MONO", "txt", "mono", "cls", "cls_lines", "cat", "ind", "value", "edge",
    "Node", "Edge", "grow", "appear", "pin", "logos", "title_card", "end_card", "example_box", "Voice", "until",
    "SPEC_URL", "STATUS", "MODULE", "folder", "hud", "tag", "note_box",
]

# The address shown everywhere (decided 2026-10-20), and the status of the 2023 edition
SPEC_URL = "https://www.w3.org/TR/vocab-ssn-2023/"
STATUS = "2023 Edition · W3C Candidate Recommendation"

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"

# ------------------------------------------------------------- the frame
m.config.pixel_width, m.config.pixel_height = 1920, 1080
m.config.frame_rate = 25
m.config.background_color = m.WHITE

# ------------------------------------------------------------- the page (W3C TR 2021 CSS)
INK = "#000000"
HEADING = "#005A9C"          # h1-h3
LINK = "#034575"
LINK_UNDERLINE = "#707070"
TOC_BG = "#F7F8F9"
ACTIVE = "#CC0000"           # the only wrong thing
OGC_BLUE = "#0070C8"         # sampled from ssn/images/OGC-0.png
GREY = "#595959"
LIGHTGREY = "#999999"        # the context, in the spec's diagrams
RULE = "#D0D0D0"

FONT = "Noto Sans"
MONO = "DejaVu Sans Mono"

# ------------------------------------------------------------- the modules (SSN-core-modules.svg)
MODULE = {
    "actuation": "#E5CCFF", "observation": "#FFCCCC", "sampling": "#FFE599", "common": "#FFFFCC",
    "all": "#B3B3B3", "sosa_core": "#ECECEC", "ssn_core": "#CCCCCC",
}

# ------------------------------------------------------------- the graph (Notation-ClassKey.svg)
# category: (fill, border)
CAT = {
    "execution": ("#E1D5E7", "#9673A6"),     # Observation, Actuation, Sampling, Deployment ~ prov:Activity
    "procedure": ("#F8CECC", "#B85450"),     # ~ prov:Plan
    "system": ("#FFE6CC", "#D79B00"),        # Sensor, Actuator, Sampler, Platform ~ prov:Agent
    "feature": ("#FFFF88", "#36393D"),       # FeatureOfInterest, Sample ~ prov:Entity
    "property": ("#D5E8D4", "#82B366"),
    "value": ("#EEEEEE", "#36393D"),
    "individual": ("#CCE5FF", "#36393D"),
    "class": ("#FFFFFF", "#000000"),
    "context": ("#FFFFFF", "#999999"),
}

for _cls in (m.VMobject, m.Text, m.Line, m.DashedLine, m.Arrow, m.Dot, m.Circle, m.Rectangle, m.Polygon):
    _cls.set_default(color=INK)


def txt(s: str, size: float = 30, color: str = INK, **kw) -> m.Text:
    """Page text, in Noto Sans; `size` as manimgx `font_size`."""
    return m.Text(s, font=FONT, font_size=size, color=color, **kw)


def mono(s: str, size: float = 26, color: str = INK, **kw) -> m.Text:
    return m.Text(s, font=MONO, font_size=size, color=color, **kw)


# ------------------------------------------------------------- the nodes
class Node(m.VGroup):
    """A box of the graph: `box` (the fill and its border), `label` (the text).
    Arrows attach to the edge of `box`."""

    def __init__(self, box: m.VMobject, border: m.VMobject, label: m.VMobject) -> None:
        super().__init__(box, border, label)
        self.box, self.border, self.label = box, border, label

    def anchor(self, toward: np.ndarray) -> np.ndarray:
        """The point on the box edge in the direction of `toward`."""
        c = self.box.get_center()
        d = np.asarray(toward, float) - c
        w, h = self.box.width / 2, self.box.height / 2
        if abs(d[0]) < 1e-9 and abs(d[1]) < 1e-9:
            return c
        k = min(w / abs(d[0]) if abs(d[0]) > 1e-9 else np.inf, h / abs(d[1]) if abs(d[1]) > 1e-9 else np.inf)
        return c + d * k


def _box(label: m.VMobject, fill: str, stroke: str, dotted: bool, pad=(0.35, 0.22), min_w=1.6,
         stroke_width: float = 3) -> Node:
    w = max(label.width + 2 * pad[0], min_w)
    h = label.height + 2 * pad[1]
    box = m.Rectangle(width=w, height=h, stroke_width=0, fill_color=fill, fill_opacity=1)
    outline = m.Rectangle(width=w, height=h, color=stroke, stroke_width=stroke_width)
    border = m.DashedVMobject(outline, num_dashes=int((w + h) * 12), dashed_ratio=0.45) if dotted else outline
    border.move_to(box)
    label.move_to(box)
    # the label stays in front of its box, even when it arrives through a transform
    box.set_z_index(1)
    border.set_z_index(2)
    label.set_z_index(3)
    return Node(box, border, label)


def cls(name: str, size: float = 30, context: bool = False) -> Node:
    """A class: white box, solid black stroke (grey if it is context)."""
    fill, stroke = CAT["context" if context else "class"]
    return _box(txt(name, size, LIGHTGREY if context else INK), fill, stroke, dotted=False)


def ind(iri: str, cat: str, size: float = 24, sub: str | None = None, icon: m.VMobject | None = None) -> Node:
    """An individual: fill of its category, dotted border, identifier in mono,
    and, if given, a label below (`sub`). `icon`: a thumbnail
    above the identifier (the real thing, scaled down: `label[0]`)."""
    fill, stroke = CAT[cat]
    label = mono(iri, size)
    if sub:
        label = m.VGroup(label, txt(sub, size * 0.8, GREY)).arrange(m.DOWN, buff=0.12)
    if icon is not None:
        label = m.VGroup(icon, label).arrange(m.DOWN, buff=0.15)
    return _box(label, fill, stroke, dotted=True)


def cat(name: str, category: str, size: float = 28, min_w: float = 2.6) -> Node:
    """A category of the spec's legend (Notation-ClassKey.svg, on the right):
    fill and stroke of its colour, solid stroke, name in Noto Sans."""
    fill, stroke = CAT[category]
    return _box(txt(name, size), fill, stroke, dotted=False, min_w=min_w)


def cls_lines(*names: str, size: float = 30) -> Node:
    """A class with several names (an individual of two classes, seen from above)."""
    label = m.VGroup(*[txt(n, size) for n in names]).arrange(m.DOWN, buff=0.1)
    return _box(label, *CAT["class"], dotted=False)


def value(s: str, size: float = 26) -> Node:
    """A value (literal, quantity, time): grey box, dotted border."""
    return ind(s, "value", size)


# ------------------------------------------------------------- the arrows
class Edge(m.VGroup):
    def __init__(self, line: m.VMobject, tip_line: m.Arrow, label: m.VMobject | None) -> None:
        parts = [line, tip_line] + ([label] if label is not None else [])
        super().__init__(*parts)
        self.line, self.tip_line, self.label = line, tip_line, label


def _bbox(mob: m.Mobject, pad: float = 0.0) -> tuple[float, float, float, float]:
    (x0, y0, _), (x1, y1, _) = mob.get_corner(m.DL), mob.get_corner(m.UR)
    return x0 - pad, y0 - pad, x1 + pad, y1 + pad


def _hits(r, s) -> bool:
    return not (r[2] < s[0] or s[2] < r[0] or r[3] < s[1] or s[3] < r[1])


def edge(a: Node, b: Node, name: str | None = None, dashed: bool = True, size: float = 24,
         color: str = "#333333", side: float = 1, label_pos: float = 0.5, open_tip: bool = False,
         avoid: list[m.Mobject] = ()) -> Edge:
    """A property from `a` to `b`: dashed between individuals (`dashed`), solid
    between classes; `open_tip` for a subclass. The label, in italics, is
    placed beside the line: first at the middle (`label_pos`) on side `side` (+1 =
    left of the direction), then elsewhere along the line and on the other side, until
    it touches neither box nor anything in `avoid`."""
    p, q = a.anchor(b.box.get_center()), b.anchor(a.box.get_center())
    tip = m.ArrowTriangleTip if open_tip else m.StealthTip
    arrow = m.Arrow(p, q, buff=0.04, stroke_width=3, color=color, tip_shape=tip,
                    max_tip_length_to_length_ratio=0.12)
    if dashed:
        body = m.DashedLine(p, arrow.get_end(), dash_length=0.12, stroke_width=3, color=color)
        arrow.set_stroke(opacity=0)             # keep only the tip
        arrow.tip.set_stroke(opacity=1)
    else:
        body = m.VMobject()
    label = None
    if name:
        label = txt(name, size, color, slant=m.ITALIC)
        d = q - p
        n = np.array([-d[1], d[0], 0.0]) / (np.linalg.norm(d) + 1e-9)
        # beside the line, without touching it: the label's half-width seen along the normal
        gap = abs(n[0]) * label.width / 2 + abs(n[1]) * label.height / 2 + 0.1
        others = [_bbox(x.box if isinstance(x, Node) else x, 0.06) for x in (a, b, arrow.tip, *avoid)]
        tries = [(t, sd) for t in (label_pos, 0.62, 0.38, 0.72, 0.28, 0.8, 0.2) for sd in (side, -side)]

        def overlap(t, sd) -> float:
            label.move_to(p + d * t + n * sd * gap)
            r = _bbox(label)
            return sum(max(0, min(r[2], o[2]) - max(r[0], o[0])) * max(0, min(r[3], o[3]) - max(r[1], o[1]))
                       for o in others)

        # the first free spot, otherwise the one with the least overlap
        best = next((ts for ts in tries if overlap(*ts) == 0), None) or min(tries, key=lambda ts: overlap(*ts))
        overlap(*best)
    return Edge(body, arrow, label)


# ------------------------------------------------------------- the animations
def appear(n: Node, run_time: float = 0.8) -> m.Animation:
    """A node appearing: the fill, then the border being drawn, then the text."""
    return m.AnimationGroup(m.FadeIn(n.box), m.Create(n.border), m.Write(n.label),
                            lag_ratio=0.25, run_time=run_time)


def grow(e: Edge, run_time: float = 0.8) -> m.Animation:
    """An arrow leaving its source and reaching its target, then its label."""
    anims = [m.Create(e.line) if len(e.line.points) else m.Wait(0), m.GrowArrow(e.tip_line)]
    out = [m.AnimationGroup(*anims)]
    if e.label is not None:
        out.append(m.FadeIn(e.label, shift=0.05 * m.UP))
    return m.Succession(*out, run_time=run_time)


# ------------------------------------------------------------- the cards
def logos(height: float = 0.9) -> m.Group:
    """The W3C and OGC logos, side by side."""
    # no stroke: the style gives vector objects a black stroke by default,
    # which framed the logo's white background
    w3c = m.SVGMobject(str(DATA / "logos" / "w3c.svg"), height=height, stroke_width=0)
    ogc = m.ImageMobject(str(REPO / "ssn" / "images" / "OGC-0.png")).set(height=height * 1.15)
    return m.Group(w3c, ogc).arrange(m.RIGHT, buff=0.35)


def title_card(episode: str, module: str, status: str = STATUS) -> m.Group:
    """The header of a TR: logos, title in `#005A9C`, status, episode."""
    lg = logos(1.0).to_corner(m.UL, buff=0.7)
    t = txt("Semantic Sensor Network Ontology", 52, HEADING, weight=m.BOLD)
    t.next_to(lg, m.DOWN, buff=0.8, aligned_edge=m.LEFT)
    status = txt(status, 30, HEADING).next_to(t, m.DOWN, buff=0.3, aligned_edge=m.LEFT)
    rule = m.Line(m.LEFT, m.RIGHT, color=RULE, stroke_width=2).set(width=12.6)
    rule.next_to(status, m.DOWN, buff=0.5, aligned_edge=m.LEFT)
    ep = txt(episode, 44, INK).next_to(rule, m.DOWN, buff=0.5, aligned_edge=m.LEFT)
    mod = txt(module, 30, GREY).next_to(ep, m.DOWN, buff=0.25, aligned_edge=m.LEFT)
    return m.Group(lg, t, status, rule, ep, mod)


def end_card(url: str = SPEC_URL) -> m.Group:
    lg = logos(0.9)
    lines = m.VGroup(
        txt("Specification", 26, GREY), txt(url, 30, LINK),
        txt("Repository and issues", 26, GREY), txt("github.com/w3c/sdw-sosa-ssn", 30, LINK),
        txt("Comments", 26, GREY), txt("public-sdw-comments@w3.org", 30, LINK),
    ).arrange(m.DOWN, buff=0.18, aligned_edge=m.LEFT)
    for i in (2, 4):
        lines[i].shift(0.25 * m.DOWN)
        lines[i + 1].shift(0.25 * m.DOWN)
    return m.Group(lg, lines).arrange(m.DOWN, buff=0.8, aligned_edge=m.LEFT).move_to(m.ORIGIN)


def hud(module: str) -> m.VGroup:
    """An episode's HUD: the module at top left, the spec address at the bottom."""
    return m.VGroup(txt(module, 24, HEADING).to_corner(m.UL, buff=0.4),
                    txt(SPEC_URL, 20, LINK).to_corner(m.DL, buff=0.35))


def folder(name: str, fill: str, width: float = 3.0, height: float = 2.0, size: float = 26,
           body: m.VMobject | None = None) -> m.VGroup:
    """A folder of the module diagram (like a UML package): the tab
    carries the name, in bold; `body`, if given, is placed inside the folder."""
    name_t = txt(name, size, INK, weight=m.BOLD)
    tab = m.Rectangle(width=max(name_t.width + 0.5, width * 0.4), height=name_t.height + 0.3,
                      fill_color=fill, fill_opacity=1, color="#333333", stroke_width=2)
    box = m.Rectangle(width=width, height=height, fill_color=fill, fill_opacity=1, color="#333333", stroke_width=2)
    tab.next_to(box, m.UP, buff=0).align_to(box, m.LEFT)
    name_t.move_to(tab)
    g = m.VGroup(box, tab, name_t)
    if body is not None:
        body.move_to(box)
        g.add(body)
    g.box, g.tab, g.name = box, tab, name_t
    return g


def tag(s: str, size: float = 24, color: str = INK, fill: str = TOC_BG) -> m.VGroup:
    """A rounded tag, with the TR table-of-contents background."""
    t = txt(s, size, color)
    bg = m.RoundedRectangle(width=t.width + 0.4, height=t.height + 0.25, corner_radius=0.12,
                            fill_color=fill, fill_opacity=1, color=RULE, stroke_width=1.5)
    t.move_to(bg)
    return m.VGroup(bg, t)


def note_box(title: str, lines: list[str], size: float = 26, kind: str = "note") -> m.VGroup:
    """A respec `.note` (green) or `.issue` (red) box, text in Noto Sans."""
    border, fill, head_c = {"note": ("#52E052", "#E9FBE9", "#1B6E1B"),
                            "issue": ("#E05252", "#FBE9E9", "#831616")}[kind]
    head = txt(title, size * 1.05, head_c, weight=m.BOLD)
    body = m.VGroup(head, *[txt(l, size) for l in lines]).arrange(m.DOWN, buff=0.18, aligned_edge=m.LEFT)
    bg = m.Rectangle(width=body.width + 0.9, height=body.height + 0.6, stroke_width=0, fill_color=fill, fill_opacity=1)
    bar = m.Rectangle(width=0.1, height=bg.height, stroke_width=0, fill_color=border, fill_opacity=1)
    bar.align_to(bg, m.LEFT).align_to(bg, m.UP)
    body.move_to(bg).shift(0.1 * m.RIGHT)
    return m.VGroup(bg, bar, body)


def pin(scene: m.Scene, *mobs: m.Mobject) -> None:
    """Pins objects to the screen (HUD, legend): they keep their place and
    size when the camera moves or zooms. `add_fixed_in_frame_mobjects`
    does not do this in a 2D scene (manimgx 0.1.1)."""
    frame = scene.camera.frame
    w0, c0 = frame.width, frame.get_center().copy()
    for mob in mobs:
        off, mw = mob.get_center() - c0, mob.width

        def follow(x, off=off, mw=mw):
            k = frame.width / w0
            x.set(width=mw * k).move_to(frame.get_center() + off * k)

        mob.add_updater(follow)
        scene.add(mob)


def example_box(code: str, caption: str = "Example", size: float = 22) -> m.VGroup:
    """A respec `.example` box: left border `#E0CB52`, background `#FCFAEE`,
    caption in `#574B0F`, code in mono. `box.line(i)` returns the glyphs of
    line i (to colour it when the voice talks about it)."""
    # a single text: lines keep their spacing and indentation
    # (non-breaking spaces, which Typst keeps); an empty line keeps its height
    src = [l.replace(" ", "\u00a0") if l.strip() else "\u00a0" for l in code.splitlines()]
    text = mono("\n".join(src), size)
    spans, k = [], 0
    for l in src:
        n = sum(1 for c in l if not c.isspace())
        spans.append((k, k + n))
        k += n
    head = txt(caption, size * 1.05, "#574B0F", weight=m.BOLD)
    body = m.VGroup(head, text).arrange(m.DOWN, buff=0.3, aligned_edge=m.LEFT)
    bg = m.Rectangle(width=body.width + 0.9, height=body.height + 0.6, stroke_width=0,
                     fill_color="#FCFAEE", fill_opacity=1)
    bar = m.Rectangle(width=0.1, height=bg.height, stroke_width=0, fill_color="#E0CB52", fill_opacity=1)
    bar.align_to(bg, m.LEFT).align_to(bg, m.UP)
    body.move_to(bg).shift(0.1 * m.RIGHT)
    box = m.VGroup(bg, bar, body)
    box.text = text
    box.line = lambda i: m.VGroup(*text.submobjects[spans[i][0]:spans[i][1]])
    return box


# ------------------------------------------------------------- the voice
class Voice:
    """The narration's timings, read from the narration pipeline's `timeline.json`
    (`narration/timeline.py`, realigned by `render.py --align-only`).
    `NARRATION_TIMELINE` points to it; `video/narrated.sh` sets it.

    A script marker is a gesture `{do: mark, id: …, cue: word}`: `at(id)`
    returns the moment the word is spoken."""

    def __init__(self, path: str | None = None) -> None:
        path = path or os.environ.get("NARRATION_TIMELINE")
        if not path or not Path(path).exists():
            raise SystemExit("no timeline.json: run video/narrated.sh, or set NARRATION_TIMELINE")
        self.tl = json.loads(Path(path).read_text())
        self.end = self.tl["audio_end"]

    def at(self, mark: str) -> float:
        for e in self.tl["events"]:
            if e.get("id") == mark:
                return e["t"]
        raise KeyError(f"no mark '{mark}' in the episode script")

    def line(self, i: int) -> tuple[float, float]:
        ln = next(x for x in self.tl["lines"] if x.get("i") == i)
        return ln["t0"], ln["t1"]


def until(scene: m.Scene, t: float) -> None:
    """Waits, in the scene, until time t of the voice."""
    if t > scene.time + 1e-3:
        scene.wait(t - scene.time)
