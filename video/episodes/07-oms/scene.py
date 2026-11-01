"""Episode 7 · OMS: observation collections, and SOSA as the RDF implementation of ISO 19156.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/07-oms/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/07-oms/episode.yaml           MP4

The observation of Vienna and the many like it; the collection that carries
what they share; the time series of timeseries-oc.ttl folding into a curve;
OMS (ISO 19156:2023) and the ogc-ms:implements links of sosa-oms.ttl; the
terms the OMS module adds.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from charter import _box  # noqa: E402

# The graph of episode 2, without its times
P = {
    "obs": m.LEFT * 0.3 + m.UP * 0.4,
    "t99": m.LEFT * 5.0 + m.UP * 2.65,
    "air": m.RIGHT * 4.6 + m.UP * 2.75,
    "shw": m.LEFT * 5.2 + m.DOWN * 2.35,
    "val": m.RIGHT * 5.0 + m.DOWN * 1.7,
}
# timeseries-oc.ttl: the members, their minutes and their results (m/s)
SERIES = [("ex:t1", "20:00", 3.24), ("ex:t2", "20:01", 3.21), ("ex:t3", "20:02", 3.15), ("ex:t4", "20:03", 3.15)]
CHART_X, CHART_Y = (-4.5, 4.5), (-2.6, -0.4)          # the chart, in scene units
V0, V1 = 3.10, 3.30                                    # its vertical scale, in m/s

TURTLE = """\
ex:ts159c a sosa:ObservationCollection ;
  sosa:hasFeatureOfInterest ex:station223 ;
  sosa:observedProperty ex:p1 ;
  sosa:madeBySensor ex:fooglemeter39 ;
  qudt:hasUnit unit:M-PER-SEC ;
  sosa:hasMember ex:t1 , ex:t2 , ex:t3 , ex:t4 .

ex:t1 a sosa:Observation ;
  sosa:phenomenonTime [ a time:Instant ;
    time:inXSDDateTime "2017-04-15T20:00:00+00:00"^^xsd:dateTime ] ;
  sosa:hasSimpleResult 3.24 ."""

# sosa-oms.ttl: a SOSA term, and the OMS requirement it implements
IMPLEMENTS = [("sosa:Observation", "obs-cpt:Observation"),
              ("sosa:madeBySensor", "obs-cpt:Observation/observer-sem"),
              ("sosa:ObservationCollection", "obs-basic:ObservationCollection"),
              ("sosa:Sample", "sam-cpt:Sample")]


def ghost(n: Node, k: int, step: np.ndarray) -> m.VGroup:
    """A copy of a node's box, without its text, behind it: another observation like it."""
    g = m.VGroup(n.box.copy(), n.border.copy()).shift(step * k)
    g.set_z_index(0).set_opacity(max(0.25, 0.85 - 0.12 * k))
    return g


def frame(around: m.Mobject, cat: str, pad: float = 0.35) -> Node:
    """A dotted box of category `cat` around a group: a collection drawn around its members."""
    fill, stroke = CAT[cat]
    r = m.Rectangle(width=around.width + 2 * pad, height=around.height + 2 * pad, stroke_width=0,
                    fill_color=fill, fill_opacity=0.45).move_to(around)
    outline = m.Rectangle(width=r.width, height=r.height, color=stroke, stroke_width=3).move_to(r)
    border = m.DashedVMobject(outline, num_dashes=int((r.width + r.height) * 12), dashed_ratio=0.45)
    r.set_z_index(-2)
    border.set_z_index(-1)
    return Node(r, border, m.VGroup())


def requirement(s: str) -> Node:
    """An OMS requirement: a UML element, white box with the OGC blue border, its name in mono."""
    return _box(mono(s, 20, OGC_BLUE), m.WHITE, OGC_BLUE, dotted=False)


def chart_xy(i: int, val: float) -> np.ndarray:
    x = CHART_X[0] + i / (len(SERIES) - 1) * (CHART_X[1] - CHART_X[0])
    y = CHART_Y[0] + (val - V0) / (V1 - V0) * (CHART_Y[1] - CHART_Y[0])
    return np.array([x, y, 0.0])


class Episode07(m.Scene):
    def construct(self) -> None:
        v = Voice()

        # --- the title card
        card = title_card("Episode 7 · OMS", "Observations, measurements and samples (ISO 19156)")
        self.add(card)
        until(self, v.at("back") - 0.4)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the graph of episode 2
        band = hud("Collections · OMS")
        obs = ind("ex:SHW_T_1872-04-04T15", "execution", sub="an observation").move_to(P["obs"])
        t99 = ind("ex:T99", "system", sub="mercury thermometer").move_to(P["t99"])
        air = ind("ex:airTemperature", "property").move_to(P["air"])
        shw = ind("ex:SHW", "feature", sub="Station Hohe Warte").move_to(P["shw"])
        val = value("22.5 °C").move_to(P["val"])
        nodes = [obs, t99, air, shw, val]
        # the other observations, behind it: the labels keep clear of them from the start
        step = np.array([0.12, -0.1, 0])
        ghosts = m.VGroup(*[ghost(obs, k, step) for k in range(1, 5)])
        vghosts = m.VGroup(*[ghost(val, k, step) for k in range(1, 5)])
        stack = nodes + [ghosts, vghosts]
        e_sensor = edge(obs, t99, "madeBySensor", side=-1, avoid=stack)
        e_prop = edge(obs, air, "observedProperty", avoid=stack + [e_sensor.label])
        e_foi = edge(obs, shw, "hasFeatureOfInterest", side=-1, avoid=stack + [e_sensor.label, e_prop.label])
        e_res = edge(obs, val, "hasResult", avoid=stack + [e_sensor.label, e_prop.label, e_foi.label])
        where = txt("Episode 2 · Vienna, 4 April 1872", 24, GREY).move_to([0, -3.0, 0])
        self.play(m.FadeIn(band), appear(obs), m.FadeIn(where), run_time=0.9)
        pin(self, band)
        self.play(m.LaggedStart(*[appear(n, 0.6) for n in nodes[1:]], lag_ratio=0.2),
                  m.LaggedStart(*[grow(e, 0.6) for e in (e_sensor, e_prop, e_foi, e_res)], lag_ratio=0.2),
                  run_time=1.6)

        # --- not alone: other observations, behind it
        until(self, v.at("alone"))
        self.play(m.LaggedStart(*[m.FadeIn(g) for g in ghosts], lag_ratio=0.25), run_time=1.2)
        until(self, v.at("again"))
        self.play(m.LaggedStart(*[m.FadeIn(g) for g in vghosts], lag_ratio=0.25), m.FadeOut(where), run_time=1.0)

        # the same three arrows, drawn again from each of them
        until(self, v.at("same"))
        # the labels step aside while the grey arrows run beside theirs
        labels = m.VGroup(e_sensor.label, e_prop.label, e_foi.label, e_res.label)
        fans = m.VGroup()
        for g in ghosts:
            src = Node(g[0], g[1], m.VGroup())
            for tgt in (t99, air, shw):
                e = edge(src, tgt, None, color=LIGHTGREY)
                fans.add(m.VGroup(e.line, e.tip_line).set_z_index(-1))
        self.play(m.FadeOut(labels), m.LaggedStart(*[m.Create(f) for f in fans], lag_ratio=0.05), run_time=1.6)
        until(self, v.at("change"))
        self.play(m.Indicate(m.VGroup(val, vghosts), color=HEADING, scale_factor=1.05), run_time=1.0)

        # --- the collection: what they share, said once
        until(self, v.at("collection"))
        coll = frame(m.VGroup(obs, ghosts), "execution", pad=0.22)
        coll_l = txt("an ObservationCollection", 22, CAT["execution"][1]).next_to(coll.box, m.UP, buff=0.12)
        self.play(m.FadeOut(fans), m.FadeIn(coll.box), m.Create(coll.border), run_time=1.0)
        until(self, v.at("once"))
        rule = note_box("A rule of sosa:ObservationCollection",
                        ["one value on the collection:", "the same value on every member"], 18).move_to([1.05, -2.95, 0])
        avoid = stack + [coll.box, coll_l, rule]
        c_sensor = edge(coll, t99, "madeBySensor", side=-1, avoid=avoid)
        c_prop = edge(coll, air, "observedProperty", avoid=avoid + [c_sensor.label])
        c_foi = edge(coll, shw, "hasFeatureOfInterest", side=1, avoid=avoid + [c_sensor.label, c_prop.label])
        c_res = edge(obs, val, "hasResult", avoid=avoid + [c_sensor.label, c_prop.label, c_foi.label])
        # its name comes with the arrows it takes over: before, it would sit on their labels
        olds, news = (e_sensor, e_prop, e_foi, e_res), (c_sensor, c_prop, c_foi, c_res)
        self.play(m.FadeIn(coll_l),
                  *[m.ReplacementTransform(m.VGroup(o.line, o.tip_line), m.VGroup(n.line, n.tip_line))
                    for o, n in zip(olds, news)],
                  *[m.FadeIn(n.label) for n in news], run_time=1.2)
        shared = m.VGroup(c_sensor, c_prop, c_foi)
        self.play(m.Indicate(shared, color=HEADING, scale_factor=1.02), run_time=0.8)

        # --- the rule
        until(self, v.at("rule"))
        self.play(m.FadeIn(rule, shift=0.1 * m.UP), run_time=0.8)
        until(self, v.at("every"))
        self.play(m.LaggedStart(*[m.Indicate(g, color=HEADING, scale_factor=1.04) for g in [obs, *ghosts]],
                                lag_ratio=0.15), run_time=1.4)

        # --- the time series of the spec
        until(self, v.at("speed"))
        vienna = m.VGroup(*nodes, ghosts, vghosts, coll, coll_l, shared, c_res, rule)
        ts = ind("ex:ts159c", "execution", sub="an ObservationCollection").move_to([0, 1.25, 0])
        sen = ind("ex:fooglemeter39", "system").move_to([-4.6, 2.6, 0])
        prop = ind("ex:p1", "property", sub="in m/s").move_to([0, 3.05, 0])
        foi = ind("ex:station223", "feature").move_to([4.6, 2.6, 0])
        top = [ts, sen, prop, foi]
        s_e = [edge(ts, sen, "madeBySensor", size=22, side=-1, avoid=top),
               edge(ts, prop, "observedProperty", size=22, avoid=top),
               edge(ts, foi, "hasFeatureOfInterest", size=22, avoid=top)]
        members = [ind(i, "execution", 22, sub=t).move_to([chart_xy(k, V0)[0], -0.85, 0])
                   for k, (i, t, _) in enumerate(SERIES)]
        m_e = [edge(ts, mb, "hasMember" if k == 0 else None, size=22, side=1, avoid=top + members)
               for k, mb in enumerate(members)]
        results = [value(f"{r}", 22).move_to([chart_xy(k, V0)[0], -2.35, 0]) for k, (_, _, r) in enumerate(SERIES)]
        r_e = [edge(mb, rb, None) for mb, rb in zip(members, results)]
        self.play(m.FadeOut(vienna), run_time=0.6)
        self.play(appear(ts), *[appear(n) for n in top[1:]], *[grow(e) for e in s_e], run_time=1.4)
        self.play(m.LaggedStart(*[m.AnimationGroup(grow(e, 0.5), appear(mb, 0.6)) for e, mb in zip(m_e, members)],
                                lag_ratio=0.25), run_time=1.6)
        until(self, v.at("results"))
        self.play(m.LaggedStart(*[m.AnimationGroup(grow(e, 0.4), appear(rb, 0.5)) for e, rb in zip(r_e, results)],
                                lag_ratio=0.25), run_time=1.4)

        # the members fold into a curve
        until(self, v.at("series"))
        axis_x = m.Line([CHART_X[0] - 0.6, CHART_Y[0], 0], [CHART_X[1] + 0.4, CHART_Y[0], 0], stroke_width=2,
                        color="#333333")
        axis_y = m.Line([CHART_X[0] - 0.6, CHART_Y[0], 0], [CHART_X[0] - 0.6, CHART_Y[1] + 0.3, 0], stroke_width=2,
                        color="#333333")
        xt = m.VGroup(*[mono(t, 18, GREY).move_to(chart_xy(k, V0) + 0.3 * m.DOWN) for k, (_, t, _) in enumerate(SERIES)])
        yt = m.VGroup(*[mono(f"{y:.2f}", 18, GREY).next_to(np.array([CHART_X[0] - 0.6, chart_xy(0, y)[1], 0]), m.LEFT,
                                                             buff=0.12) for y in (3.10, 3.20, 3.30)])
        unit = txt("m/s", 20, GREY).next_to(axis_y, m.UP, buff=0.1)
        dots = [m.Dot(chart_xy(k, r), radius=0.09, color=CAT["execution"][1]) for k, (_, _, r) in enumerate(SERIES)]
        curve = m.VMobject(color=CAT["execution"][1], stroke_width=4).set_points_as_corners(
            [chart_xy(k, r) for k, (_, _, r) in enumerate(SERIES)])
        nums = m.VGroup(*[mono(f"{r}", 18).next_to(d, m.UP, buff=0.12) for d, (_, _, r) in zip(dots, SERIES)])
        self.play(m.FadeOut(m.VGroup(*members, *m_e, *r_e)), m.Create(axis_x), m.Create(axis_y), m.FadeIn(xt),
                  m.FadeIn(yt), m.FadeIn(unit), *[m.ReplacementTransform(rb, d) for rb, d in zip(results, dots)],
                  run_time=1.2)
        self.play(m.Create(curve), m.FadeIn(nums), run_time=1.0)

        # --- OMS, ISO 19156:2023
        until(self, v.at("oms"))
        series = m.VGroup(*top, *s_e, axis_x, axis_y, xt, yt, unit, *dots, curve, nums)
        doc = m.VGroup(txt("ISO 19156:2023", 34, INK, weight=m.BOLD),
                       txt("Geographic information —", 26), txt("Observations, measurements", 26),
                       txt("and samples", 26)).arrange(m.DOWN, buff=0.15, aligned_edge=m.LEFT)
        page = m.Rectangle(width=doc.width + 1.0, height=doc.height + 1.0, fill_color=m.WHITE, fill_opacity=1,
                           color=LIGHTGREY, stroke_width=2)
        doc.move_to(page)
        book = m.VGroup(page, doc).move_to([-2.6, 0.2, 0])
        oms = txt("OMS", 60, OGC_BLUE, weight=m.BOLD).next_to(book, m.RIGHT, buff=0.9)
        also = txt("OGC Abstract Specification Topic 20", 22, GREY).next_to(oms, m.DOWN, buff=0.25)
        also.align_to(oms, m.LEFT)
        self.play(m.FadeOut(series), run_time=0.6)
        self.play(m.FadeIn(oms, shift=0.1 * m.UP), run_time=0.7)
        until(self, v.at("iso"))
        self.play(m.FadeIn(book, shift=0.2 * m.RIGHT), m.FadeIn(also), run_time=0.9)

        # --- UML on one side, RDF on the other, linked by ogc-ms:implements
        until(self, v.at("uml"))
        left = [requirement(r).move_to([-3.6, y, 0]) for (_, r), y in zip(IMPLEMENTS, (1.5, 0.4, -0.7, -1.8))]
        right = [cls(s_, 24).move_to([3.6, y, 0]) for (s_, _), y in zip(IMPLEMENTS, (1.5, 0.4, -0.7, -1.8))]
        h_l = txt("OMS · UML requirements", 26, OGC_BLUE, weight=m.BOLD).move_to([-3.6, 2.6, 0])
        h_r = txt("SOSA · RDF", 26, HEADING, weight=m.BOLD).move_to([3.6, 2.6, 0])
        self.play(m.FadeOut(m.VGroup(book, oms, also)), run_time=0.5)
        self.play(m.FadeIn(h_l), m.LaggedStart(*[appear(n, 0.5) for n in left], lag_ratio=0.2), run_time=1.2)
        until(self, v.at("rdf"))
        self.play(m.FadeIn(h_r), m.LaggedStart(*[appear(n, 0.5) for n in right], lag_ratio=0.2), run_time=1.2)
        until(self, v.at("implements"))
        imp = [edge(r, l_, "ogc-ms:implements" if k == 0 else None, dashed=False, size=22)
               for k, (r, l_) in enumerate(zip(right, left))]
        self.play(m.LaggedStart(*[grow(e, 0.6) for e in imp], lag_ratio=0.25), run_time=1.4)
        until(self, v.at("pairs"))
        for r, l_ in zip(right, left):
            self.play(m.Indicate(m.VGroup(r, l_), color=HEADING, scale_factor=1.03), run_time=0.45)
        until(self, v.at("counterpart"))
        self.play(*[m.ShowPassingFlash(e.tip_line.copy().set_stroke(HEADING, width=8, opacity=1), time_width=0.6)
                    for e in imp], run_time=1.0)

        # --- the terms the OMS module adds
        until(self, v.at("nomatch"))
        pairs = m.VGroup(*left, *right, *imp, h_l, h_r)
        head = m.VGroup(mono("sosa-oms:", 28, HEADING), txt("terms added by the OMS module", 26, GREY))
        head.arrange(m.RIGHT, buff=0.3).move_to([0, 2.7, 0])
        self.play(m.FadeOut(pairs), run_time=0.6)
        self.play(m.FadeIn(head, shift=0.1 * m.DOWN), run_time=0.7)
        rows = []
        for (a, prop_, b), y in zip((("ObservationCollection", "sosa-oms:madeOnPlatform", "Platform"),
                                     ("MaterialSample", "sosa-oms:storageLocation", "a location"),
                                     ("Sample", "sosa-oms:hasPreparationStep", "sosa-oms:PreparationStep")),
                                    (1.75, 0.6, -0.55)):
            na = cls(a, 26).move_to([-4.3, y, 0])
            nb = cls(b, 26, context=(b == "a location"))
            nb.move_to([6.6 - nb.width / 2, y, 0])
            rows.append((na, nb, edge(na, nb, prop_, dashed=False, size=22)))
        for mark, (na, nb, e) in zip(("platform", "stored", "steps"), rows):
            until(self, v.at(mark))
            self.play(appear(na, 0.6), grow(e, 0.7), appear(nb, 0.6), run_time=1.0)
        until(self, v.at("normative"))
        note = note_box("Note", ["the sosa-oms: terms are not normative in the 2023 edition,",
                                 "pending more implementation experience"], 22).move_to([0.6, -2.15, 0])
        self.play(m.FadeIn(note, shift=0.1 * m.UP), run_time=0.8)

        # --- the Turtle
        until(self, v.at("turtle"))
        added = m.VGroup(head, note, *[x for r in rows for x in r])
        ex = example_box(TURTLE, "Example · timeseries-oc.ttl (abridged)", 20)
        self.play(m.FadeOut(added), run_time=0.6)
        ex.set(width=min(ex.width, 13.0)).move_to(0.15 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("carries"))
        for i in (1, 2, 3):
            self.play(ex.mark(i), run_time=0.25)
        until(self, v.at("lists"))
        self.play(ex.mark(5), run_time=0.3)

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
