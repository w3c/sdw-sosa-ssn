"""Episode 6 · System capabilities: what a sensor can do, and where it survives.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/06-system/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/06-system/episode.yaml           MP4

The thermometer of Vienna, whose precision the data does not give; the
InkBird and its data sheet; the capabilities (IBS-TH2-PLUS-capabilities.ttl)
as an observation collection about the sensor itself, with its validity
context; the operating conditions (InkBird-IBS-TH2-survivable-conditions.ttl,
InkBird-IBS-TH2-Range.ttl) on a temperature scale; the 2017 classes replaced
by observations and two sample vocabularies.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from charter import _box  # noqa: E402

TURTLE = """\
ex:InkBird-IBS-TH2-0354313547 a ex:InkBird-IBS-TH2 ;
  sosa:hasOperatingConditions ex:IBSTH2SurvivalRange .

ex:IBSTH2SurvivalRange a sosa:ObservationCollection , sosa:SurvivableConditions ;
  sosa:hasMember [
    sosa:observedProperty sosa-env:MinAmbientTemperature ;
    sosa:hasResult [ qudt:value -273.0 ; qudt:hasUnit unit:DEG_C ] ;
  ] , [
    sosa:observedProperty sosa-env:MaxAmbientTemperature ;
    sosa:hasResult [ qudt:value 80.0 ; qudt:hasUnit unit:DEG_C ] ;
  ] ."""

# the temperature scale of the operating conditions, in °C → scene x
T0, T1, X0, X1 = -300.0, 100.0, -6.0, 6.0
AXIS_Y = -1.9


def tx(t: float) -> float:
    return X0 + (t - T0) / (T1 - T0) * (X1 - X0)


def device() -> m.VGroup:
    """The InkBird IBS-TH2 Plus, line-drawn: a white case, its screen, its button."""
    body = m.RoundedRectangle(width=2.3, height=2.6, corner_radius=0.35, fill_color=m.WHITE, fill_opacity=1,
                              color="#333333", stroke_width=3)
    screen = m.Rectangle(width=1.75, height=1.25, fill_color="#DDE6D3", fill_opacity=1, color="#333333",
                         stroke_width=2).move_to(body.get_center() + 0.35 * m.UP)
    t = mono("21.4°C", 30).move_to(screen.get_center() + 0.17 * m.UP)
    h = mono("45%", 22, GREY).next_to(t, m.DOWN, buff=0.08)
    button = m.Circle(radius=0.12, color="#333333", stroke_width=2).move_to(body.get_center() + 0.75 * m.DOWN)
    brand = txt("INKBIRD", 16, GREY, weight=m.BOLD).next_to(button, m.DOWN, buff=0.1)
    return m.VGroup(body, screen, t, h, button, brand)


def sheet() -> m.VGroup:
    """A data sheet: a page, its title, three rows (the values of IBS-TH2-PLUS-capabilities.ttl)."""
    head = txt("IBS-TH2 Plus · data sheet", 24, HEADING, weight=m.BOLD)
    rows = [("Temperature accuracy", "±0.5 °C"), ("Measuring range", "−40 … 60 °C"),
            ("Valid for humidity", "0 … 99 % RH")]
    names = m.VGroup(*[txt(a, 22) for a, _ in rows]).arrange(m.DOWN, buff=0.3, aligned_edge=m.LEFT)
    vals = m.VGroup(*[mono(b, 22) for _, b in rows])
    for n, val in zip(names, vals):
        val.next_to(n, m.RIGHT, buff=0.5).align_to(n, m.DOWN)
    vals.align_to(vals[0], m.RIGHT)
    x_right = max(val.get_right()[0] for val in vals)
    for val in vals:
        val.shift((x_right - val.get_right()[0]) * m.RIGHT)
    table = m.VGroup(names, vals)
    rule = m.Line(m.LEFT, m.RIGHT, color=RULE, stroke_width=2).set(width=table.width)
    body = m.VGroup(head, rule, table).arrange(m.DOWN, buff=0.3, aligned_edge=m.LEFT)
    page = m.Rectangle(width=body.width + 0.8, height=body.height + 0.8, fill_color=m.WHITE, fill_opacity=1,
                       color=LIGHTGREY, stroke_width=2)
    body.move_to(page)
    return m.VGroup(page, body)


def member(prop: str, val: str, size: float = 16) -> Node:
    """A member of a collection: an observation (dotted, execution colour) holding its observed
    property and its result."""
    chips = m.VGroup(ind(prop, "property", size), value(val, size)).arrange(m.RIGHT, buff=0.25)
    return _box(chips, *CAT["execution"], dotted=True, pad=(0.2, 0.15))


def stack(nodes: list[Node], center: np.ndarray) -> m.VGroup:
    g = m.VGroup(*nodes).arrange(m.DOWN, buff=0.22)
    return g.move_to(center)


def beside(a: Node, b: Node, name: str, off: np.ndarray, color: str = HEADING) -> Edge:
    """A property from `a` to `b`, drawn parallel to the arrow between them, shifted by `off`
    (as in episode 5). The label goes on the far side."""
    p, q = a.anchor(b.box.get_center()) + off, b.anchor(a.box.get_center()) + off
    arrow = m.Arrow(p, q, buff=0.04, stroke_width=3, color=color, tip_shape=m.StealthTip,
                    max_tip_length_to_length_ratio=0.12)
    body = m.DashedLine(p, arrow.get_end(), dash_length=0.12, stroke_width=3, color=color)
    arrow.set_stroke(opacity=0)
    arrow.tip.set_stroke(opacity=1)
    label = txt(name, 22, color, slant=m.ITALIC)
    u = off / (np.linalg.norm(off) + 1e-9)
    label.move_to((p + q) / 2 + u * (abs(u[0]) * label.width / 2 + abs(u[1]) * label.height / 2 + 0.1))
    return Edge(body, arrow, label)


def frame_of(g: m.Mobject) -> Node:
    """A node standing for a group (a collection's members): its bounding box, nothing drawn."""
    r = m.Rectangle(width=g.width, height=g.height, stroke_width=0).move_to(g)
    return Node(r, r, m.VGroup())


class Episode06(m.Scene):
    def construct(self) -> None:
        v = Voice()

        # --- the title card
        card = title_card("Episode 6 · System capabilities", "What a sensor can do, and where it survives")
        self.add(card)
        until(self, v.at("vienna") - 0.4)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the thermometer of Vienna: how precise?
        band = hud("System capabilities")
        t99 = ind("ex:T99", "system", sub="mercury thermometer").move_to([-2.0, 0.6, 0])
        where = txt("Episode 2 · Vienna, 4 April 1872", 26, GREY).next_to(t99, m.DOWN, buff=0.6)
        self.play(m.FadeIn(band), appear(t99), m.FadeIn(where), run_time=0.9)
        pin(self, band)
        until(self, v.at("precise"))
        q = txt("± ? °C", 44, GREY).next_to(t99.box, m.RIGHT, buff=0.8)
        self.play(m.FadeIn(q, scale=1.3), run_time=0.7)
        until(self, v.at("say"))
        self.play(m.Indicate(q, color=ACTIVE, scale_factor=1.1), run_time=0.9)

        # --- the InkBird and its data sheet
        until(self, v.at("sheet"))
        dev = device().move_to([-3.8, 0.1, 0])
        page = sheet().move_to([2.4, 0.1, 0])
        self.play(m.FadeOut(m.VGroup(t99, where, q)), run_time=0.5)
        self.play(m.FadeIn(page, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("small"))
        self.play(m.FadeIn(dev, shift=0.2 * m.RIGHT), run_time=0.8)
        self.play(m.Indicate(dev[1], color=HEADING, scale_factor=1.05), run_time=0.8)

        # --- two things: capabilities, operating conditions
        until(self, v.at("two"))
        sensor = cls("Sensor").move_to([0, 2.1, 0])
        oc_l = cls("ObservationCollection").move_to([-3.8, -0.9, 0])
        oc_r = cls("ObservationCollection").move_to([3.8, -0.9, 0])
        e_cap = edge(sensor, oc_l, "hasSystemCapability", dashed=False, side=1)
        e_op = edge(sensor, oc_r, "hasOperatingConditions", dashed=False, side=-1)
        can = txt("what it can do", 26, GREY).next_to(oc_l.box, m.DOWN, buff=0.3)
        work = txt("where it can work", 26, GREY).next_to(oc_r.box, m.DOWN, buff=0.3)
        self.play(m.FadeOut(dev), m.FadeOut(page), run_time=0.5)
        self.play(appear(sensor), run_time=0.7)
        until(self, v.at("capabilities"))
        self.play(grow(e_cap), appear(oc_l), m.FadeIn(can), run_time=1.0)
        until(self, v.at("conditions"))
        self.play(grow(e_op), appear(oc_r), m.FadeIn(work), run_time=1.0)

        # --- the capabilities: an observation collection about the sensor
        until(self, v.at("observation"))
        two = m.VGroup(sensor, oc_l, oc_r, e_cap, e_op, can, work)
        # a column on the left (sensor, its capabilities, their context), the members on the right
        s = ind("ex:IBS-TH2-Plus-T-687343", "system", 22, sub="InkBird IBS-TH2 Plus").move_to([-4.0, 2.55, 0])
        caps = ind("sensor:IBS-TH2-Plus-T-systemCapability", "execution", 17,
                   sub="an ObservationCollection").move_to([-4.0, 0.45, 0])
        has_cap = edge(s, caps, "hasSystemCapability", side=-1, size=22)
        foi = beside(s, caps, "isFeatureOfInterestOf", 0.35 * m.RIGHT)
        entailed = txt("entailed by hasSystemCapability", 18, HEADING).next_to(foi.label, m.DOWN, buff=0.08)
        entailed.align_to(foi.label, m.LEFT)
        mem = [member("sosa-cap:TemperatureAccuracy", "0.5 °C", 14),
               member("sosa-cap:MaxMeasurableTemperature", "60.0 °C", 14),
               member("sosa-cap:MinMeasurableTemperature", "-40.0 °C", 14)]
        col = stack(mem, [3.6, 1.0, 0])
        has_mem = edge(caps, frame_of(col), "hasMember", side=-1, size=20, avoid=[foi.label, entailed])
        self.play(m.FadeOut(two), run_time=0.5)
        self.play(appear(s), appear(caps), grow(has_cap), run_time=1.2)
        until(self, v.at("accuracy"))
        self.play(grow(has_mem, 0.6), appear(mem[0], 0.7), run_time=1.0)
        until(self, v.at("measures"))
        self.play(m.LaggedStart(appear(mem[1], 0.7), appear(mem[2], 0.7), lag_ratio=0.4), run_time=1.1)

        # --- the feature of interest is the sensor itself
        until(self, v.at("itself"))
        self.play(grow(foi, 0.9), run_time=0.9)
        self.play(m.FadeIn(entailed), s.border.animate.set_stroke(CAT["feature"][1]),
                  s.box.animate.set_fill(CAT["feature"][0], opacity=1), run_time=0.8)

        # --- the validity context
        until(self, v.at("context"))
        ctx = ind("sensor:IBS-TH2-Plus-T-normalHumidityConditions", "execution", 15).move_to([-3.95, -1.75, 0])
        validity = edge(caps, ctx, "hasValidityContext", side=1, size=22)
        self.play(appear(ctx, 0.8), run_time=0.8)
        until(self, v.at("humidity"))
        cmem = [member("sosa-env:MinAmbientRelativeHumidity", "0.0 %", 14),
                member("sosa-env:MaxAmbientRelativeHumidity", "99.0 %", 14)]
        ccol = stack(cmem, [3.6, -2.2, 0])
        c_mem = edge(ctx, frame_of(ccol), "hasMember", side=1, size=20)
        self.play(grow(c_mem, 0.6), m.LaggedStart(*[appear(c, 0.7) for c in cmem], lag_ratio=0.4), run_time=1.1)
        until(self, v.at("validity"))
        self.play(grow(validity), run_time=0.9)

        # --- the operating conditions, on a temperature scale
        until(self, v.at("operating"))
        caps_all = m.VGroup(s, caps, has_cap, has_mem, col, foi, entailed, ctx, validity, ccol, c_mem)
        inst = ind("ex:InkBird-IBS-TH2-0354313547", "system", 22, sub="InkBird IBS-TH2").move_to([-3.6, 2.55, 0])
        surv = ind("ex:IBSTH2SurvivalRange", "execution", 22, sub="SurvivableConditions").move_to([-3.6, 0.55, 0])
        has_op = edge(inst, surv, "hasOperatingConditions", side=1)
        self.play(m.FadeOut(caps_all), run_time=0.6)
        self.play(appear(inst), appear(surv), grow(has_op), run_time=1.2)
        until(self, v.at("environment"))
        axis = m.Arrow([X0 - 0.2, AXIS_Y, 0], [X1 + 0.5, AXIS_Y, 0], buff=0, stroke_width=3, color="#333333",
                       tip_shape=m.StealthTip, max_tip_length_to_length_ratio=0.03)
        ticks = m.VGroup()
        for t in (-273, -40, 0, 60, 80):
            ticks.add(m.Line([tx(t), AXIS_Y - 0.1, 0], [tx(t), AXIS_Y + 0.1, 0], stroke_width=2, color="#333333"))
            ticks.add(mono(f"{t}".replace("-", "−"), 20, GREY).move_to([tx(t), AXIS_Y - 0.35, 0]))
        unit = txt("ambient temperature, °C", 20, GREY).next_to(axis, m.DOWN, buff=0.45).align_to(axis, m.LEFT)
        self.play(m.GrowArrow(axis), m.FadeIn(ticks), m.FadeIn(unit), run_time=1.0)

        def band_(t_a: float, t_b: float, h: float, fill: str, stroke: str) -> m.Rectangle:
            r = m.Rectangle(width=tx(t_b) - tx(t_a), height=h, fill_color=fill, fill_opacity=1, color=stroke,
                            stroke_width=2)
            return r.move_to([(tx(t_a) + tx(t_b)) / 2, AXIS_Y + h / 2 + 0.02, 0])

        until(self, v.at("normally"))
        normal = band_(-40, 60, 0.95, "#DFF0D8", "#82B366")
        normal_l = txt("NormalOperatingConditions", 22, "#3C763D").next_to(normal, m.UP, buff=0.15)
        self.play(m.GrowFromEdge(normal, m.DOWN), m.FadeIn(normal_l), run_time=0.9)
        until(self, v.at("survives"))
        survive = band_(-273, 80, 0.55, "#FFF3CD", "#D79B00").set_z_index(-1)
        survive_l = txt("SurvivableConditions", 22, "#8A6D3B").move_to([tx(-160), AXIS_Y + 0.85, 0])
        self.play(m.GrowFromEdge(survive, m.DOWN), m.FadeIn(survive_l),
                  m.Indicate(surv, color=CAT["execution"][1], scale_factor=1.04), run_time=1.0)
        until(self, v.at("serviceable"))
        lost = band_(80, 100, 0.55, "#FBE9E9", ACTIVE)
        lost_l = txt("no longer serviceable", 20, ACTIVE).next_to(axis, m.DOWN, buff=0.45).align_to(axis, m.RIGHT)
        self.play(m.FadeIn(lost), m.FadeIn(lost_l), run_time=0.8)
        until(self, v.at("suboptimal"))
        sub = note_box("SuboptimalOperatingConditions", ["results still reported, less precise",
                                                         "(not in this example)"], 20).move_to([3.4, 1.6, 0])
        self.play(m.FadeIn(sub, shift=0.1 * m.UP), run_time=0.8)

        # --- no new boxes: observations, and two vocabularies
        until(self, v.at("boxes"))
        cond = m.VGroup(inst, surv, has_op, axis, ticks, unit, normal, normal_l, survive, survive_l, lost, lost_l, sub)
        old = m.VGroup(*[cls(n, 26, context=True) for n in ("SystemProperty", "OperatingProperty",
                                                              "SurvivalProperty")]).arrange(m.RIGHT, buff=0.6)
        old.move_to([0, 2.3, 0])
        y2017 = txt("2017 edition", 22, GREY).next_to(old, m.DOWN, buff=0.2)
        strikes = m.VGroup(*[m.Line(o.get_left(), o.get_right(), stroke_width=4, color=ACTIVE) for o in old])
        self.play(m.FadeOut(cond), run_time=0.6)
        self.play(m.LaggedStart(*[appear(o, 0.6) for o in old], lag_ratio=0.25), m.FadeIn(y2017), run_time=1.0)
        self.play(m.LaggedStart(*[m.Create(x) for x in strikes], lag_ratio=0.25), run_time=0.8)
        until(self, v.at("collections"))
        new = m.VGroup(cls("Observation"), cls("ObservationCollection")).arrange(m.RIGHT, buff=1.2).move_to([0, 2.5, 0])
        self.play(m.FadeOut(m.VGroup(old, strikes, y2017)), run_time=0.5)
        self.play(m.LaggedStart(*[appear(n, 0.7) for n in new], lag_ratio=0.3), run_time=1.0)
        until(self, v.at("vocabularies"))
        cols = []
        for x, prefix, what, names in (
                (-3.4, "sosa-cap:", "system capabilities",
                 ("Accuracy", "Precision", "Resolution", "ResponseTime", "Drift")),
                (3.4, "sosa-env:", "system environment",
                 ("AmbientTemperature", "AmbientHumidity", "Altitude", "WindSpeed", "Salinity"))):
            head = m.VGroup(mono(prefix, 24, HEADING), txt(what, 22, GREY)).arrange(m.RIGHT, buff=0.25)
            chips = m.VGroup(*[ind(n, "property", 20) for n in names]).arrange(m.DOWN, buff=0.1)
            cols.append(m.VGroup(head, chips).arrange(m.DOWN, buff=0.3).move_to([x, -0.5, 0]))
        self.play(*[m.FadeIn(c[0]) for c in cols], run_time=0.5)
        self.play(*[m.LaggedStart(*[appear(n, 0.5) for n in c[1]], lag_ratio=0.2) for c in cols], run_time=1.6)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · InkBird-IBS-TH2-survivable-conditions.ttl (abridged)", 20)
        self.play(m.FadeOut(m.VGroup(new, *cols)), run_time=0.6)
        ex.set(width=min(ex.width, 13.4)).move_to(0.15 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("collection"))
        self.play(ex.mark(3), run_time=0.3)
        until(self, v.at("members"))
        for i in (5, 6, 8, 9):
            self.play(ex.mark(i), run_time=0.22)

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
