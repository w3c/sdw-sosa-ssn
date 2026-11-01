"""Episode 9 · Alignments: where the colours come from, and SOSA among other ontologies.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/09-alignments/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/09-alignments/episode.yaml           MP4

The colour key of the spec's diagrams (Notation-ClassKey.svg), similar to that
of PROV-O; the PROV alignment (sosa-prov.ttl), each category under its PROV
class; the other alignments of the chapter Alignments, each card giving what
becomes of sosa:FeatureOfInterest; the SSSOM spreadsheet
(sosa-mappings-sssom.xlsx), its rows for sosa:FeatureOfInterest.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403

# the PROV-O documentation's colours and shapes: an Entity is a yellow ellipse,
# an Activity a blue rectangle, an Agent an orange pentagon
PROV = {"entity": ("#FFFC87", "#808080"), "activity": ("#9FB1FC", "#0000FF"), "agent": ("#FED37F", "#000000")}

# the legend (left) and the PROV classes (right), row by row
ROWS = {"execution": 2.3, "system": 1.2, "feature": 0.1, "property": -1.0, "procedure": -2.1}
LEGEND = [("execution", "Observation, Actuation, Sampling"), ("system", "Sensor, Actuator, Sampler"),
          ("feature", "FeatureOfInterest, Sample"), ("property", "Property"), ("procedure", "Procedure")]

# what becomes of sosa:FeatureOfInterest in each alignment (the alignment files, the SSSOM sheet)
CARDS = {
    "upper": [("DUL", "DOLCE UltraLite", "⊑ dul:Entity"),
              ("DOLCE", "upper ontology", "⊑ Endurant ⊔ Perdurant"),
              ("BFO · CCO", "Basic Formal Ontology", "⊑ obo:BFO_0000001"),
              ("PROV-O", "provenance", "⊑ prov:Entity")],
    "application": [("SAREF", "ETSI · smart applications", "⊑ saref:FeatureOfInterest"),
                    ("IDO", "Industrial Data Ontology", "⊑ lis:Object"),
                    ("OBOE", "observations in ecology", "⊑ oboe-core:Entity")],
    "apis": [("SensorThings", "OGC API · JSON", "↔ Feature"),
             ("Connected Systems", "OGC API · JSON", "↔ Feature")],
}
GROUPS = {"upper": "upper level ontologies", "application": "application ontologies", "apis": "APIs, not RDF"}
CARD_X = (-5.22, -1.74, 1.74, 5.22)
CARD_Y = {"upper": 2.0, "application": -0.1, "apis": -2.2}

# sosa-mappings-sssom.xlsx: the rows of sosa:FeatureOfInterest, one per sheet
SSSOM = [("sosa:FeatureOfInterest", "rdfs:subClassOf", "prov:Entity"),
         ("sosa:FeatureOfInterest", "rdfs:subClassOf", "dul:Entity"),
         ("sosa:FeatureOfInterest", "rdfs:subClassOf", "obo:BFO_0000001"),
         ("sosa:FeatureOfInterest", "rdfs:subClassOf", "saref:FeatureOfInterest"),
         ("sosa:FeatureOfInterest", "rdfs:subClassOf", "lis:Object"),
         ("sosa:FeatureOfInterest", "rdfs:subClassOf", "oboe:Entity")]

TURTLE = """\
sosa:Observation
  rdfs:subClassOf prov:Activity ;
.
sosa:Procedure
  rdfs:subClassOf prov:Plan ;
.
sosa:FeatureOfInterest
  rdfs:subClassOf prov:Entity ;
.
sosa:isSampleOf
  rdfs:subPropertyOf prov:wasDerivedFrom ;
."""


def prov(name: str, kind: str, size: float = 28) -> Node:
    """A PROV class in the PROV-O documentation's notation."""
    fill, stroke = PROV[kind]
    label = txt(name, size)
    w, h = max(label.width + 0.7, 2.2), label.height + 0.5
    if kind == "entity":
        shape = m.Ellipse(width=w + 0.4, height=h + 0.15)
    elif kind == "activity":
        shape = m.Rectangle(width=w, height=h)
    else:
        shape = m.Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 4, 0], [0, h / 2 + 0.25, 0],
                          [-w / 2, h / 4, 0])
    box = shape.copy().set_fill(fill, 1).set_stroke(width=0)
    border = shape.copy().set_fill(opacity=0).set_stroke(stroke, 3)
    label.move_to(box)
    box.set_z_index(1)
    border.set_z_index(2)
    label.set_z_index(3)
    return Node(box, border, label)


def card(name: str, what: str, maps: str, width: float = 3.42) -> m.VGroup:
    """An alignment: its name, what it is, and what becomes of the yellow box there."""
    swatch = m.Rectangle(width=0.3, height=0.22, fill_color=CAT["feature"][0], fill_opacity=1,
                         color=CAT["feature"][1], stroke_width=1.5)
    line = m.VGroup(swatch, mono(maps, 14)).arrange(m.RIGHT, buff=0.1)
    body = m.VGroup(txt(name, 24, INK, weight=m.BOLD), txt(what, 18, GREY), line)
    body.arrange(m.DOWN, buff=0.12, aligned_edge=m.LEFT)
    bg = m.RoundedRectangle(width=width, height=1.35, corner_radius=0.12, fill_color=TOC_BG, fill_opacity=1,
                            color=RULE, stroke_width=1.5)
    body.move_to(bg).align_to(bg.get_left() + 0.18 * m.RIGHT, m.LEFT)
    c = m.VGroup(bg, body)
    c.line = line
    return c


def sssom_table() -> m.VGroup:
    """The SSSOM rows: a header and one row per sheet, in mono, ruled like the TR tables."""
    head = ("subject_id", "predicate_id", "object_id")
    cols = [m.VGroup(*[mono(r[i], 18, HEADING if k == 0 else INK) for k, r in enumerate([head, *SSSOM])])
            for i in range(3)]
    for c in cols:
        c.arrange(m.DOWN, buff=0.28, aligned_edge=m.LEFT)
    grid = m.VGroup(*cols).arrange(m.RIGHT, buff=0.6, aligned_edge=m.UP)
    for k in range(1, len(SSSOM) + 1):         # the cells of a row on one baseline
        for c in cols[1:]:
            c[k].align_to(cols[0][k], m.UP)
    rules = m.VGroup(*[m.Line(grid.get_left() + 0.2 * m.LEFT, grid.get_right() + 0.2 * m.RIGHT, stroke_width=1.5,
                              color=RULE).move_to([grid.get_center()[0], (cols[0][k].get_bottom()[1] +
                                                                         cols[0][k + 1].get_top()[1]) / 2, 0])
                       for k in range(len(SSSOM))])
    t = m.VGroup(rules, grid)
    t.rows = [m.VGroup(*[c[k] for c in cols]) for k in range(1, len(SSSOM) + 1)]
    return t


class Episode09(m.Scene):
    def construct(self) -> None:
        v = Voice()

        # --- the title card
        card_ = title_card("Episode 9 · Alignments", "SOSA and SSN among other ontologies")
        self.add(card_)
        until(self, v.at("colours") - 0.4)
        self.play(m.FadeOut(card_), run_time=0.6)

        # --- the colours of the graphs, the legend of the spec
        band = hud("Alignments")
        legend = {k: cat(name, k, 24, min_w=4.6) for k, name in LEGEND}
        for k, n in legend.items():
            n.move_to([0, ROWS[k], 0])
        self.play(m.FadeIn(band), run_time=0.5)
        pin(self, band)
        for mark, k in (("purple", "execution"), ("orange", "system"), ("yellow", "feature"), ("green", "property"),
                        ("pink", "procedure")):
            until(self, v.at(mark))
            self.play(appear(legend[k], 0.6))

        # --- PROV: the activity, the entity, the agent
        until(self, v.at("prov"))
        title = m.VGroup(txt("PROV-O", 30, HEADING, weight=m.BOLD), txt("the W3C ontology for provenance", 24, GREY))
        title.arrange(m.RIGHT, buff=0.3).move_to([3.5, 3.15, 0])
        self.play(*[n.animate.move_to([-4.1, ROWS[k], 0]) for k, n in legend.items()],
                  m.FadeIn(title, shift=0.1 * m.DOWN), run_time=1.0)
        until(self, v.at("alignment"))
        self.play(m.Indicate(m.VGroup(*legend.values()), color=HEADING, scale_factor=1.03), run_time=0.8)

        act = prov("Activity", "activity").move_to([2.0, ROWS["execution"], 0])
        ent = prov("Entity", "entity").move_to([2.0, -0.45, 0])
        agt = prov("Agent", "agent").move_to([5.75, ROWS["system"], 0])
        used = edge(act, ent, "used", dashed=False, size=22, side=1, label_pos=0.72)
        assoc = edge(act, agt, "wasAssociatedWith", dashed=False, size=22, avoid=[title, used.label])
        until(self, v.at("activity"))
        self.play(appear(act, 0.7))
        until(self, v.at("entity"))
        self.play(appear(ent, 0.7), grow(used, 0.7), run_time=1.0)
        until(self, v.at("agent"))
        self.play(appear(agt, 0.7), grow(assoc, 0.7), run_time=1.0)

        # each category under its PROV class: an open arrow, the subclass of the spec's diagrams
        def sub(k: str, target: Node) -> Edge:
            return edge(legend[k], target, None, dashed=False, open_tip=True, color=HEADING)

        until(self, v.at("acts"))
        s_exec = sub("execution", act)
        self.play(grow(s_exec, 0.8))
        until(self, v.at("agents"))
        s_sys = sub("system", agt)
        either = txt("Agent or Entity", 20, HEADING).next_to(s_sys.tip_line, m.UP, buff=0.08)
        either.set_x(0.2)
        self.play(grow(s_sys, 0.8), m.FadeIn(either), run_time=1.0)
        until(self, v.at("entities"))
        s_feat, s_prop = sub("feature", ent), sub("property", ent)
        self.play(m.LaggedStart(grow(s_feat, 0.7), grow(s_prop, 0.7), lag_ratio=0.4), run_time=1.2)
        until(self, v.at("plan"))
        plan = prov("Plan", "entity").move_to([2.0, ROWS["procedure"], 0])
        isa = edge(plan, ent, None, dashed=False, open_tip=True, color=GREY)
        s_proc = sub("procedure", plan)
        self.play(appear(plan, 0.7), grow(isa, 0.7), run_time=0.9)
        self.play(grow(s_proc, 0.8))
        classes = m.VGroup(*legend.values(), title, act, ent, agt, plan, used, assoc, isa, s_exec, s_sys,
                           either, s_feat, s_prop, s_proc)

        # --- the arrows: episodes 3 and 2
        until(self, v.at("arrows"))
        bub = ind("ex:Bubble873", "feature", 22).move_to([-4.0, 1.4, 0])
        core = ind("ex:IceCore12", "feature", 22).move_to([3.6, 1.4, 0])
        obs = ind("ex:SHW_T_1872-04-04T15", "execution", 22).move_to([-3.6, -1.6, 0])
        val = value("22.5 °C", 22).move_to([3.6, -1.6, 0])
        e_of = edge(bub, core, "sosa:isSampleOf", size=22)
        e_res = edge(obs, val, "sosa:hasResult", size=22)
        p_of = txt("⊑ prov:wasDerivedFrom", 22, HEADING, slant=m.ITALIC).next_to(e_of.line, m.DOWN, buff=0.2)
        p_res = txt("⊑ prov:generated", 22, HEADING, slant=m.ITALIC).next_to(e_res.line, m.DOWN, buff=0.2)
        self.play(m.FadeOut(classes), run_time=0.6)
        self.play(appear(bub, 0.6), appear(core, 0.6), grow(e_of, 0.8), appear(obs, 0.6), appear(val, 0.6),
                  grow(e_res, 0.8), run_time=1.2)
        until(self, v.at("derived"))
        self.play(m.FadeIn(p_of, shift=0.1 * m.DOWN), run_time=0.6)
        until(self, v.at("generated"))
        self.play(m.FadeIn(p_res, shift=0.1 * m.DOWN), run_time=0.6)
        arrows = m.VGroup(bub, core, obs, val, e_of, e_res, p_of, p_res)

        # --- the other alignments, group by group
        cards, labels = {}, {}
        for g, items in CARDS.items():
            cards[g] = [card(*it).move_to([x, CARD_Y[g], 0]) for it, x in zip(items, CARD_X)]
            labels[g] = txt(GROUPS[g], 20, HEADING).next_to(cards[g][0], m.UP, buff=0.1, aligned_edge=m.LEFT)
        until(self, v.at("other"))
        self.play(m.FadeOut(arrows), run_time=0.6)
        until(self, v.at("upper"))
        self.play(m.FadeIn(labels["upper"]),
                  m.LaggedStart(*[m.FadeIn(c, shift=0.1 * m.UP) for c in cards["upper"]], lag_ratio=0.25),
                  run_time=1.4)
        until(self, v.at("application"))
        self.play(m.FadeIn(labels["application"]), m.FadeIn(cards["application"][0], shift=0.1 * m.UP), run_time=0.7)
        until(self, v.at("ido"))
        self.play(m.FadeIn(cards["application"][1], shift=0.1 * m.UP), run_time=0.6)
        until(self, v.at("oboe"))
        self.play(m.FadeIn(cards["application"][2], shift=0.1 * m.UP), run_time=0.6)
        until(self, v.at("place"))
        lines = [c.line for g in ("upper", "application") for c in cards[g]]
        self.play(m.LaggedStart(*[m.Indicate(l_, color=HEADING, scale_factor=1.08) for l_ in lines], lag_ratio=0.12),
                  run_time=1.8)
        until(self, v.at("apis"))
        self.play(m.FadeIn(labels["apis"]),
                  m.LaggedStart(*[m.FadeIn(c, shift=0.1 * m.UP) for c in cards["apis"]], lag_ratio=0.3), run_time=1.0)
        until(self, v.at("table"))
        not_ax = tag("a table, not an axiom", 22, GREY).move_to([CARD_X[2] + 1.7, CARD_Y["apis"], 0])
        self.play(m.FadeIn(not_ax, shift=0.1 * m.LEFT), run_time=0.6)
        grid = m.VGroup(*[c for g in cards for c in cards[g]], *labels.values(), not_ax)

        # --- the SSSOM spreadsheet
        until(self, v.at("sheet"))
        table = sssom_table().move_to([0, -0.4, 0])
        name = m.VGroup(mono("sosa-mappings-sssom.xlsx", 22, LINK), txt("one sheet per alignment", 20, GREY))
        name.arrange(m.RIGHT, buff=0.35).next_to(table, m.UP, buff=0.45)
        self.play(m.FadeOut(grid), run_time=0.6)
        self.play(m.FadeIn(name, shift=0.1 * m.DOWN), m.FadeIn(table[0]),
                  m.LaggedStart(*[m.FadeIn(r) for r in [m.VGroup(*[c[0] for c in table[1]]), *table.rows]],
                                lag_ratio=0.15), run_time=1.6)
        until(self, v.at("sssom"))
        sssom = txt("SSSOM · a Simple Standard for Sharing Ontological Mappings", 22, GREY)
        sssom.next_to(table, m.DOWN, buff=0.4)
        self.play(m.FadeIn(sssom), run_time=0.6)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · sosa-prov.ttl (abridged)", 22)
        self.play(m.FadeOut(m.VGroup(table, name, sssom)), run_time=0.5)
        ex.move_to(0.2 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("lines"))
        for i in (0, 1, 3, 4, 6, 7):
            self.play(ex.mark(i), run_time=0.2)
        until(self, v.at("subprop"))
        for i in (9, 10):
            self.play(ex.mark(i), run_time=0.25)

        # --- the end
        until(self, v.at("end_module"))
        fin = end_card()
        self.play(m.FadeOut(ex), m.FadeOut(band), run_time=0.6)
        self.play(m.FadeIn(fin), run_time=0.8)
        until(self, v.at("tuned"))
        nxt = txt("Stay tuned for more", 30, HEADING)
        nxt.to_edge(m.DOWN, buff=0.7)
        self.play(m.FadeIn(nxt, shift=0.1 * m.UP))
        until(self, v.end + 2.0)
