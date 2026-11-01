"""Episode 5 · SSN: the axioms behind the boxes.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/05-ssn/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/05-ssn/episode.yaml           MP4

The graph of episode 2, read with SOSA (hints, the named inverse), then with
SSN: the nodes lose their type, and the owl:allValuesFrom restrictions of
ssn-observation.ttl give it back, by inference. Then why the rules are local,
the disjoint collections (ssn.ttl), and SSN importing SOSA.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403

# The graph of episode 2, without its times, in scene units (14.2 x 8 frame)
P = {
    "obs": m.UP * 0.4,
    "t99": m.LEFT * 5.4 + m.UP * 2.5,
    "shw": m.LEFT * 5.0 + m.DOWN * 1.4,
    "air": m.RIGHT * 5.0 + m.UP * 2.4,
    "val": m.RIGHT * 5.0 + m.DOWN * 1.0,
}
BOTTOM = m.DOWN * 2.7 + m.RIGHT * 2.2   # the notes and rules, under the graph, clear of the address

TURTLE = """\
# SOSA (sosa-observation.ttl): hints, and the inverse
sosa:madeBySensor schema:domainIncludes sosa:Observation ;
  schema:rangeIncludes sosa:Sensor ;
  owl:inverseOf sosa:madeObservation .

# SSN (ssn-observation.ttl): an axiom
sosa:Observation rdfs:subClassOf [ a owl:Restriction ;
  owl:onProperty sosa:madeBySensor ;
  owl:allValuesFrom sosa:Sensor ] ."""


def nodes(typed: bool) -> dict[str, Node]:
    """The nodes of episode 2: with their category (`typed`), or as individuals without one,
    except the observation, whose type the data gives."""
    c = (lambda k: k) if typed else (lambda k: "individual")
    return {
        "obs": ind("ex:SHW_T_1872-04-04T15", "execution", sub="an observation").move_to(P["obs"]),
        "t99": ind("ex:T99", c("system"), sub="mercury thermometer").move_to(P["t99"]),
        "shw": ind("ex:SHW", c("feature"), sub="Station Hohe Warte").move_to(P["shw"]),
        "air": ind("ex:airTemperature", c("property")).move_to(P["air"]),
        "val": value("22.5 °C").move_to(P["val"]),
    }


def beside(a: Node, b: Node, name: str, off: np.ndarray, color: str = HEADING) -> Edge:
    """A property from `a` to `b`, drawn parallel to the arrow between them, shifted by `off`:
    the inverse beside its property. The label goes on the far side, near `a`."""
    p, q = a.anchor(b.box.get_center()) + off, b.anchor(a.box.get_center()) + off
    arrow = m.Arrow(p, q, buff=0.04, stroke_width=3, color=color, tip_shape=m.StealthTip,
                    max_tip_length_to_length_ratio=0.12)
    body = m.DashedLine(p, arrow.get_end(), dash_length=0.12, stroke_width=3, color=color)
    arrow.set_stroke(opacity=0)
    arrow.tip.set_stroke(opacity=1)
    label = txt(name, 24, color, slant=m.ITALIC)
    u = off / (np.linalg.norm(off) + 1e-9)
    label.move_to(p + 0.2 * (q - p) + u * (abs(u[0]) * label.width / 2 + abs(u[1]) * label.height / 2 + 0.1))
    return Edge(body, arrow, label)


def retype(n: Node, cat: str) -> m.Animation:
    """A node taking the colour of its category: the fill and the border change, the text stays."""
    fill, stroke = CAT[cat]
    return m.AnimationGroup(n.box.animate.set_fill(fill, opacity=1), n.border.animate.set_stroke(stroke),
                            run_time=0.8)


class Episode05(m.Scene):
    def construct(self) -> None:
        v = Voice()

        # --- the title card
        card = title_card("Episode 5 · SSN", "The axioms behind SOSA")
        self.add(card)
        until(self, v.at("recall") - 0.4)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the graph of episode 2
        band = hud("SSN · the axioms")
        N = nodes(typed=True)
        obs, t99, shw, air, val = (N[k] for k in ("obs", "t99", "shw", "air", "val"))
        avoid = list(N.values())
        e_sensor = edge(obs, t99, "madeBySensor", side=-1, avoid=avoid)
        e_prop = edge(obs, air, "observedProperty", avoid=avoid + [e_sensor.label])
        e_foi = edge(obs, shw, "hasFeatureOfInterest", side=-1, avoid=avoid + [e_sensor.label, e_prop.label])
        e_res = edge(obs, val, "hasResult", avoid=avoid + [e_sensor.label, e_prop.label, e_foi.label])
        edges = [e_sensor, e_prop, e_foi, e_res]
        where = txt("Episode 2 · Vienna, 4 April 1872", 26, GREY).move_to(BOTTOM)
        self.play(m.FadeIn(band), appear(obs, 0.8), run_time=0.8)
        pin(self, band)
        self.play(m.LaggedStart(*[appear(n, 0.7) for n in (t99, air, shw, val)], lag_ratio=0.3),
                  m.FadeIn(where), run_time=1.6)
        until(self, v.at("reading"))
        self.play(m.LaggedStart(*[grow(e, 0.6) for e in edges], lag_ratio=0.3), run_time=1.6)

        # --- SOSA: the hints
        until(self, v.at("light"))
        self.play(m.Indicate(m.VGroup(*N.values()), scale_factor=1.02, color=HEADING), run_time=1.0)
        until(self, v.at("hints"))
        hint = note_box("In SOSA, a hint", ["madeBySensor: from an Observation to a Sensor"], 22).move_to(BOTTOM)
        self.play(m.FadeOut(where), m.FadeIn(hint, shift=0.1 * m.UP),
                  e_sensor.label.animate.set_color(HEADING), run_time=0.9)

        # --- SOSA: the inverse, beside its property
        until(self, v.at("inverse"))
        d = t99.box.get_center() - obs.box.get_center()
        n = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
        # beside madeBySensor, on the side away from its label
        away = -np.sign(np.dot(e_sensor.label.get_center() - e_sensor.tip_line.get_center(), n)) or 1.0
        e_inv = beside(t99, obs, "madeObservation", 0.3 * away * n)
        self.play(grow(e_inv, 1.0))
        until(self, v.at("then"))
        self.play(m.ShowPassingFlash(e_sensor.tip_line.copy().set_stroke(HEADING, width=8, opacity=1), time_width=0.6),
                  m.ShowPassingFlash(e_inv.tip_line.copy().set_stroke(HEADING, width=8, opacity=1), time_width=0.6),
                  run_time=1.2)

        # --- SSN: axioms in OWL
        until(self, v.at("simple"))
        self.play(m.FadeOut(e_inv), m.FadeOut(hint), e_sensor.label.animate.set_color("#333333"), run_time=0.8)
        until(self, v.at("axioms"))
        ssn = tag("SSN adds axioms", 26, HEADING).move_to(BOTTOM)
        self.play(m.FadeIn(ssn, shift=0.1 * m.UP), run_time=0.7)
        until(self, v.at("owl"))
        owl = tag("OWL 2 DL", 26, INK).next_to(ssn, m.RIGHT, buff=0.4)
        self.play(m.FadeIn(owl, shift=0.1 * m.UP), run_time=0.7)

        # --- the data says only one type
        until(self, v.at("suppose"))
        fill, stroke = CAT["individual"]
        self.play(m.FadeOut(ssn), m.FadeOut(owl),
                  *[m.AnimationGroup(N[k].box.animate.set_fill(fill, opacity=1), N[k].border.animate.set_stroke(stroke))
                    for k in ("t99", "shw", "air")], run_time=1.2)
        typed = note_box("The data says only", ["ex:SHW_T_1872-04-04T15 a sosa:Observation"], 22).move_to(BOTTOM)
        self.play(m.FadeIn(typed, shift=0.05 * m.UP), run_time=0.6)
        until(self, v.at("notype"))
        # on the free side of each node, away from its arrow
        unknown = m.VGroup(*[txt("?", 34, GREY).next_to(N[k].box, side, buff=0.15)
                             for k, side in (("t99", m.DOWN), ("shw", m.LEFT), ("air", m.UP))])
        unknown[0].align_to(t99.box, m.LEFT).shift(0.2 * m.RIGHT)
        self.play(m.LaggedStart(*[m.FadeIn(q, scale=1.5) for q in unknown], lag_ratio=0.3), run_time=1.0)

        # --- the rules, one by one, and what the reasoner infers
        until(self, v.at("only"))
        rules = [txt(s, 22) for s in ("madeBySensor → only a Sensor", "observedProperty → only a Property",
                                      "hasFeatureOfInterest → only a FeatureOfInterest")]
        head = txt("SSN · for an observation", 22, "#1B6E1B", weight=m.BOLD)
        body = m.VGroup(head, *rules).arrange(m.DOWN, buff=0.12, aligned_edge=m.LEFT)
        bg = m.Rectangle(width=body.width + 0.9, height=body.height + 0.5, stroke_width=0, fill_color="#E9FBE9",
                         fill_opacity=1)
        bar = m.Rectangle(width=0.1, height=bg.height, stroke_width=0, fill_color="#52E052", fill_opacity=1)
        bar.align_to(bg, m.LEFT)
        body.move_to(bg).shift(0.1 * m.RIGHT)
        box = m.VGroup(bg, bar, body).move_to(BOTTOM + 0.15 * m.DOWN)
        for r in rules:
            r.set_opacity(0).set_z_index(4)       # in front of the box, which arrives with the first rule
        self.play(m.FadeOut(typed), m.FadeIn(m.VGroup(bg, bar, head)), rules[0].animate.set_opacity(1), run_time=0.9)

        def infer(e: Edge, k: str, cat: str, q: m.Mobject) -> None:
            self.play(m.ShowPassingFlash(e.tip_line.copy().set_stroke(HEADING, width=8, opacity=1), time_width=0.6),
                      run_time=0.8)
            self.play(retype(N[k], cat), m.FadeOut(q), m.Flash(N[k].box.get_corner(m.UR), color=CAT[cat][1],
                                                              line_length=0.15), run_time=0.8)

        until(self, v.at("infers"))
        infer(e_sensor, "t99", "system", unknown[0])
        until(self, v.at("property"))
        self.play(rules[1].animate.set_opacity(1), run_time=0.4)
        infer(e_prop, "air", "property", unknown[2])
        until(self, v.at("station"))
        self.play(rules[2].animate.set_opacity(1), run_time=0.4)
        infer(e_foi, "shw", "feature", unknown[1])
        until(self, v.at("colours"))
        graph = m.VGroup(*N.values(), *edges)
        self.play(m.Indicate(graph, scale_factor=1.02, color=HEADING), run_time=1.0)

        # --- local rules: one property, three kinds of execution
        until(self, v.at("local"))
        self.play(m.FadeOut(graph), m.FadeOut(box), run_time=0.8)
        foi = cls("FeatureOfInterest").move_to([3.6, -0.3, 0])
        exes = [cls(c).move_to([-3.6, y, 0]) for c, y in (("Observation", 1.9), ("Actuation", -0.3), ("Sampling", -2.5))]
        lines_ = [edge(x, foi, "hasFeatureOfInterest", dashed=False, size=22, label_pos=0.42) for x in exes]
        rule = txt("for an observation: only a FeatureOfInterest", 22, "#1B6E1B").next_to(exes[0].box, m.UP, buff=0.2)
        self.play(appear(foi, 0.8), appear(exes[0], 0.8), grow(lines_[0]), m.FadeIn(rule), run_time=1.2)
        until(self, v.at("used"))
        self.play(*[appear(x, 0.8) for x in exes[1:]], *[grow(e) for e in lines_[1:]], run_time=1.2)
        until(self, v.at("global"))
        domain = tag("rdfs:domain sosa:Observation", 24, ACTIVE, "#FBE9E9").move_to([3.6, 1.7, 0])
        wrong = m.VGroup(*[txt("an Observation?", 20, ACTIVE).next_to(x.box, m.DOWN, buff=0.12) for x in exes[1:]])
        self.play(m.FadeIn(domain, shift=0.1 * m.DOWN), m.FadeIn(wrong), *[x.border.animate.set_stroke(ACTIVE)
                                                                           for x in exes[1:]], run_time=1.0)
        until(self, v.at("never"))
        strike = m.Line(domain.get_left(), domain.get_right(), stroke_width=4, color=ACTIVE)
        self.play(m.Create(strike), m.FadeOut(wrong), *[x.border.animate.set_stroke(INK) for x in exes[1:]],
                  run_time=0.8)

        # --- consistency: the collections are disjoint
        until(self, v.at("consistent"))
        local = m.VGroup(foi, *exes, *lines_, rule, domain, strike)
        oc = cls("ObservationCollection").move_to([-3.6, 1.6, 0])
        sc = cls("SampleCollection").move_to([3.6, 1.6, 0])
        dis = m.DashedLine(oc.box.get_right(), sc.box.get_left(), dash_length=0.12, stroke_width=3, color="#333333")
        dis_l = txt("owl:disjointWith", 22, "#333333", slant=m.ITALIC).next_to(dis, m.UP, buff=0.12)
        self.play(m.FadeOut(local), run_time=0.6)
        self.play(appear(oc, 0.8), appear(sc, 0.8), run_time=0.8)
        until(self, v.at("disjoint"))
        self.play(m.Create(dis), m.FadeIn(dis_l), run_time=0.8)
        until(self, v.at("error"))
        c1 = ind("ex:collection-1", "individual").move_to([0, -1.6, 0])
        t1 = edge(c1, oc, "rdf:type", size=22, side=-1)
        t2 = edge(c1, sc, "rdf:type", size=22, side=1)
        self.play(appear(c1, 0.6), grow(t1, 0.6), grow(t2, 0.6), run_time=1.0)
        flag = txt("inconsistent", 28, ACTIVE, weight=m.BOLD).next_to(c1.box, m.DOWN, buff=0.25)
        self.play(c1.border.animate.set_stroke(ACTIVE), c1.box.animate.set_fill("#FBE9E9", opacity=1),
                  *[x.animate.set_color(ACTIVE) for x in (t1, t2)], m.FadeIn(flag, scale=1.2), run_time=0.9)

        # --- SOSA and SSN
        until(self, v.at("share"))
        cons = m.VGroup(oc, sc, dis, dis_l, c1, t1, t2, flag)
        sosa = folder("SOSA", MODULE["sosa_core"], width=4.6, height=2.4,
                      body=m.VGroup(txt("terms and definitions,", 24), txt("hints, inverses", 24))
                      .arrange(m.DOWN, buff=0.12))
        sosa.move_to([-3.4, 0, 0])
        self.play(m.FadeOut(cons), run_time=0.6)
        self.play(m.FadeIn(sosa, shift=0.1 * m.UP), run_time=0.8)
        until(self, v.at("imports"))
        ssn_f = folder("SSN", MODULE["ssn_core"], width=4.6, height=2.4,
                       body=m.VGroup(txt("OWL axioms:", 24), txt("only, some, disjoint", 24)).arrange(m.DOWN, buff=0.12))
        ssn_f.move_to([3.4, 0, 0])
        a, b = Node(ssn_f.box, ssn_f.box, m.VGroup()), Node(sosa.box, sosa.box, m.VGroup())
        imp = edge(a, b, "imports", size=24)
        self.play(m.FadeIn(ssn_f, shift=0.1 * m.UP), run_time=0.8)
        self.play(grow(imp), run_time=0.8)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · sosa-observation.ttl and ssn-observation.ttl (abridged)", 20)
        self.play(m.FadeOut(m.VGroup(sosa, ssn_f, imp)), run_time=0.6)
        ex.set(width=min(ex.width, 13.0)).move_to(0.15 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("lines"))
        for i in (6, 7, 8):
            self.play(ex.mark(i), run_time=0.3)

        # --- the end
        until(self, v.at("module"))
        fin = end_card()
        self.play(m.FadeOut(ex), m.FadeOut(band), run_time=0.6)
        self.play(m.FadeIn(fin), run_time=0.8)
        until(self, v.at("tuned"))
        nxt = txt("Stay tuned for more", 30, HEADING)
        nxt.to_edge(m.DOWN, buff=0.7)
        self.play(m.FadeIn(nxt, shift=0.1 * m.UP))
        until(self, v.end + 2.0)
