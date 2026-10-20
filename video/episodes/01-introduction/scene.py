"""Episode 1 · Introduction: SOSA and SSN, the 2023 edition as a Candidate
Recommendation, and the series.

The voice leads (`v.at(id)`, the `mark`s of episode.yaml). Through video/narrated.sh:

    video/narrated.sh video/episodes/01-introduction/episode.yaml --dry     storyboards
    video/narrated.sh video/episodes/01-introduction/episode.yaml           MP4

The text follows the Abstract and the Introduction of the spec. The context
example is the Introduction's: a river (the Danube, near Vienna, as in
episode 2), the current speed, the sampling strategy; then a thermostat for
actuation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from globe import Globe, sensor_points  # noqa: E402

VIENNA = (16.37, 48.21)
VIEW = (16.35, 48.25)                # the centre of the Danube map
# three measurement points on the Danube: Krems, Vienna, Bratislava
STATIONS = [(15.60, 48.40, "10:00", m.DOWN), (16.40, 48.22, "10:40", m.UP), (17.11, 48.14, "11:25", m.DOWN)]
INSET = (-3.7, -0.1, 6.2, 5.8)       # the map: centre x, centre y, width, height
ZOOM = 2.6                           # the zoom-out onto the web graph
PAN = 6.0                            # the pan along the timeline

EPISODES = [
    ("2", "Observations", "Vienna, 1872"),
    ("3", "Samples", "Antarctic ice"),
    ("4", "Actuation", "Saint-Étienne"),
    ("5", "SSN axioms", "reasoning with SOSA"),
    ("6", "System capabilities", "surviving the cold"),
    ("7", "Collections", "time series since 1872"),
    ("8", "Sample relations", "slicing an ice core"),
    ("9", "Alignments", "PROV, SAREF, OMS…"),
]


def mask(cx: float, cy: float, w: float, h: float) -> m.VGroup:
    """Four white rectangles around a window: whatever extends beyond the map
    is hidden."""
    big = 40
    l, r, b, t = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    rects = [((l - big + l) / 2, 0, big, 2 * big), ((r + r + big) / 2, 0, big, 2 * big),
             (cx, (b - big + b) / 2, w, big), (cx, (t + t + big) / 2, w, big)]
    return m.VGroup(*[m.Rectangle(width=rw, height=rh, stroke_width=0, fill_color=m.WHITE, fill_opacity=1)
                      .move_to([x, y, 0]) for x, y, rw, rh in rects])


def thermostat(level: m.ValueTracker) -> tuple[m.VGroup, m.VMobject]:
    """A line-drawn thermostat: the casing, the dial, the setpoint display."""
    body = m.RoundedRectangle(width=2.6, height=2.6, corner_radius=0.35, stroke_width=3, color=INK,
                              fill_color="#FAFAFA", fill_opacity=1)
    ring = m.Circle(radius=1.0, stroke_width=3, color=INK)
    ticks = m.VGroup(*[m.Line(1.05 * np.array([np.cos(a), np.sin(a), 0]), 1.2 * np.array([np.cos(a), np.sin(a), 0]),
                              stroke_width=2, color=GREY) for a in np.radians(np.arange(-210, 31, 20))])
    caption = txt("setpoint", 18, GREY).shift(0.45 * m.DOWN)
    static = m.VGroup(body, ring, ticks, caption)
    shown = m.always_redraw(lambda: mono(f"{level.get_value():.1f} °C", 30).move_to(static.get_center() + 0.1 * m.UP))
    return static, shown


class Episode01(m.Scene):
    def construct(self) -> None:
        v = Voice()
        frame = self.camera.frame

        # --- the title card
        card = title_card("Episode 1 · Introduction", "SOSA and SSN")
        self.add(card)
        until(self, v.at("globe") - 0.7)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- sensors everywhere
        g = Globe(3.4)
        lon, lat, op = m.ValueTracker(-40), m.ValueTracker(15), m.ValueTracker(0)
        pts = sensor_points()

        def earth():
            out = g.draw(lon.get_value(), lat.get_value())
            if op.get_value() > 0.01:
                out.add(g.sensors(lon.get_value(), lat.get_value(), pts, op.get_value()))
            return out

        world = m.always_redraw(earth)
        self.play(m.FadeIn(world), op.animate.set_value(1), lon.animate.set_value(-15), run_time=2.5,
                  rate_func=m.linear)
        until(self, v.at("watch"))
        self.play(lon.animate.set_value(VIENNA[0]), lat.animate.set_value(VIENNA[1] - 6), run_time=3.5)

        # --- a number alone
        until(self, v.at("number"))
        world.clear_updaters()
        big = txt("2.4", 140, INK)
        self.play(m.FadeOut(world), run_time=0.6)
        self.play(m.FadeIn(big, scale=0.7), run_time=0.8)

        # --- the river: a map of the Danube, in a window
        cx, cy, w, h = INSET
        R = 160.0                    # one degree of longitude is about 1.9 units at this latitude
        mapg = Globe(R, center=[cx, cy, 0], detail="50m", borders=True, graticule=1)
        land = mapg.draw(*VIEW, stroke=1.4)
        danube = mapg.river(("Donau", "Danube"), *VIEW, width=5)
        frame_box = m.Rectangle(width=w, height=h, color=GREY, stroke_width=2)
        frame_box.move_to([cx, cy, 0])
        win = mask(cx, cy, w, h)
        for x in (land, danube):
            x.set_z_index(0)
        win.set_z_index(0.5)
        frame_box.set_z_index(0.6)
        # the box has the width of "2.4 m/s" from the start; the unit arrives with the property
        val = value("2.4 m/s", 30).move_to([3.6, -0.1, 0])
        full = val.label
        short = mono("2.4", 30).move_to(full).set_z_index(3)
        val.remove(full)
        val.add(short)
        val.label = short

        until(self, v.at("river"))
        self.play(m.ReplacementTransform(big, val.label), m.FadeIn(val.box), m.Create(val.border), run_time=1.0)
        self.add(land, win)
        self.play(m.FadeIn(land), m.FadeIn(frame_box), run_time=0.8)
        self.play(m.Create(danube), run_time=1.2)
        foi_ring = m.DashedVMobject(m.Rectangle(width=w + 0.16, height=h + 0.16, color=CAT["feature"][1], stroke_width=4),
                                    num_dashes=90).move_to([cx, cy, 0]).set_z_index(3)
        win_node = Node(frame_box, frame_box, m.VGroup())
        foi_name = m.VGroup(mono("ex:Danube", 24),).next_to(frame_box, m.UP, buff=0.12).set_z_index(3)
        foi_bg = m.SurroundingRectangle(foi_name, buff=0.08, stroke_width=0, fill_color=CAT["feature"][0],
                                        fill_opacity=1).set_z_index(2.5)
        e_foi = edge(val, win_node, "feature of interest", side=-1).set_z_index(4)
        self.play(m.Create(foi_ring), m.FadeIn(foi_bg), m.FadeIn(foi_name), grow(e_foi), run_time=1.2)

        until(self, v.at("velocity"))
        prop = ind("ex:flowVelocity", "property").move_to([3.6, 2.4, 0])
        e_prop = edge(val, prop, "observed property", side=-1, avoid=[frame_box]).set_z_index(4)
        self.play(m.Transform(short, full), grow(e_prop), run_time=0.9)
        self.play(appear(prop, 0.7))

        until(self, v.at("where"))
        dots = m.VGroup()
        times = m.VGroup()
        for lo, la, hh, side in STATIONS:
            p = mapg.point(*VIEW, lo, la)
            d = m.Dot(p, radius=0.09, color=CAT["system"][1]).set_z_index(0.4)
            dots.add(d)
            t_ = mono(hh, 20).next_to(d, side, buff=0.15)
            times.add(m.VGroup(m.BackgroundRectangle(t_, color=m.WHITE, fill_opacity=0.85, buff=0.05), t_)
                      .set_z_index(0.4))
        where = value("where · when", 26).move_to([3.6, -2.6, 0])
        e_where = edge(val, where, "sampling strategy", side=1, avoid=[frame_box]).set_z_index(4)
        self.play(m.LaggedStart(*[m.FadeIn(d, scale=2.5) for d in dots], lag_ratio=0.3),
                  m.LaggedStart(*[m.FadeIn(t) for t in times], lag_ratio=0.3), grow(e_where, 0.9), run_time=0.9)
        self.play(appear(where, 0.6))

        # --- a thermostat
        until(self, v.at("thermostat"))
        context = m.Group(land, danube, win, frame_box, foi_ring, foi_name, foi_bg, e_foi, val, prop, e_prop,
                          dots, times, where, e_where)
        self.play(m.FadeOut(context), run_time=0.7)
        setp = m.ValueTracker(19.0)
        th_static, th_shown = thermostat(setp)
        therm = m.VGroup(th_static).move_to([-4.0, -0.3, 0])
        self.play(m.Create(th_static, lag_ratio=0.1), m.FadeIn(th_shown), run_time=1.2)
        until(self, v.at("setpoint"))
        self.play(setp.animate.set_value(21.0), run_time=1.6)
        until(self, v.at("acted"))
        act = ind("an actuation", "execution").move_to([1.6, 1.6, 0])
        th_ring = m.DashedVMobject(m.Rectangle(width=3.0, height=3.0, color=CAT["feature"][1], stroke_width=4),
                                   num_dashes=60).move_to(th_static)
        th_node = Node(th_ring, th_ring, m.VGroup())
        e_act = edge(act, th_node, "feature of interest", side=1)
        self.play(appear(act, 0.7))
        self.play(m.Create(th_ring), grow(e_act), run_time=1.0)
        until(self, v.at("changed"))
        sp = ind("ex:setpoint", "property", sub="temperature setpoint").move_to([4.6, -1.6, 0])
        e_sp = edge(act, sp, "actuated property", side=-1)
        self.play(grow(e_sp), appear(sp, 0.8), run_time=1.2)

        # --- what SSN describes: the colour legend of the spec
        until(self, v.at("sensors") - 0.5)
        self.play(m.FadeOut(m.VGroup(th_static, th_shown, act, th_ring, e_act, sp, e_sp)), run_time=0.6)
        band = hud("SOSA and SSN · Introduction")
        self.play(m.FadeIn(band), run_time=0.4)
        pin(self, band)
        rows = [("Sensor", "Observation"), ("Actuator", "Actuation"), ("Sampler", "Sampling")]
        left, mid, arrows = [], [], []
        for k, (a, b) in enumerate(rows):
            y = 1.7 - 1.7 * k
            mid.append(cat(b, "execution").move_to([0.2, y, 0]))
            left.append(cat(a, "system").move_to([-4.6, y, 0]))
            arrows.append(edge(mid[-1], left[-1], None, dashed=False))
        for k, key in enumerate(("sensors", "actuators", "samplers")):
            until(self, v.at(key))
            self.play(appear(left[k], 0.6), appear(mid[k], 0.6), grow(arrows[k], 0.6), run_time=0.9)
        group = m.DashedVMobject(m.RoundedRectangle(width=3.4, height=5.1, corner_radius=0.2, color=GREY,
                                                   stroke_width=2), num_dashes=60).move_to([0.2, 0, 0])
        gnode = Node(group, group, m.VGroup())
        right = {"procedures": cat("Procedure", "procedure").move_to([4.8, 2.2, 0]),
                 "features": cat("FeatureOfInterest, Sample", "feature", size=24).move_to([4.8, 0, 0]),
                 "properties": cat("Property", "property").move_to([4.8, -2.2, 0])}
        for key, n in right.items():
            until(self, v.at(key))
            e = edge(gnode, n, None, dashed=False)
            arrows.append(e)
            anims = [m.Create(group)] if key == "procedures" else []
            self.play(*anims, grow(e, 0.6), appear(n, 0.6), run_time=0.9)
        diagram = m.VGroup(*left, *mid, group, *right.values(), *arrows)

        # --- SOSA, within SSN
        until(self, v.at("minimal"))
        self.play(diagram.animate.scale(0.62).move_to([1.7, -0.8, 0]), run_time=1.2)
        sosa = folder("SOSA", MODULE["sosa_core"], width=diagram.width + 0.7, height=diagram.height + 0.7)
        sosa.move_to(diagram).shift(0.05 * m.DOWN)
        sosa_ns = mono("http://www.w3.org/ns/sosa/", 18, GREY).next_to(sosa.tab, m.RIGHT, buff=0.3)
        for x in sosa:
            x.set_z_index(-1)
        until(self, v.at("sosa"))
        expand = txt("Sensor, Observation, Sample, Actuator", 24, GREY).next_to(sosa.box, m.DOWN, buff=0.15)
        self.play(m.FadeIn(sosa), m.FadeIn(sosa_ns), m.FadeIn(expand, shift=0.1 * m.UP), run_time=1.0)
        until(self, v.at("interoperability"))
        self.play(m.Circumscribe(sosa.box, color=HEADING, buff=0.08), run_time=1.2)
        until(self, v.at("axioms"))
        ssn = folder("SSN", MODULE["ssn_core"], width=13.0, height=5.8)
        ssn.move_to([0, -0.35, 0])
        for x in ssn:
            x.set_z_index(-2)
        ssn_ns = mono("http://www.w3.org/ns/ssn/", 18, GREY).next_to(ssn.tab, m.RIGHT, buff=0.3)
        syms = m.VGroup(*[m.MathTex(s, color=INK).scale(1.3) for s in
                          (r"\sqsubseteq", r"\equiv", r"\exists", r"\forall", r"\sqcap", r"^{-1}")])
        spots = [(-5.6, 1.4), (-4.6, 0.6), (-5.7, -0.4), (-4.7, -1.3), (-5.6, -2.3), (-4.6, -3.0)]
        for s_, (x, y) in zip(syms, spots):
            s_.move_to([x, y, 0])
        self.play(m.FadeIn(ssn), m.FadeIn(ssn_ns), m.FadeOut(expand), run_time=1.0)
        self.play(m.LaggedStart(*[m.FadeIn(s_, scale=1.6) for s_ in syms], lag_ratio=0.2), run_time=1.6)
        modules = m.VGroup(ssn, ssn_ns, syms, sosa, sosa_ns, diagram)

        # --- W3C, OGC, SAREF
        until(self, v.at("joint"))
        self.play(modules.animate.scale(0.42).move_to([0, -1.9, 0]), m.FadeOut(ssn_ns), m.FadeOut(sosa_ns), run_time=1.2)
        hub = Node(modules[0].box, modules[0].box, m.VGroup())
        lg = logos(0.9).move_to([0, 2.6, 0])
        self.play(m.FadeIn(lg, shift=0.1 * m.DOWN), run_time=0.8)
        sources = {"ogc": tag("OGC · Sensor Web Enablement", 22, OGC_BLUE).move_to([-4.5, 0.9, 0]),
                   "w3c": tag("W3C · Semantic Web, Linked Data", 22, HEADING).move_to([0.4, 0.9, 0]),
                   "saref": tag("ETSI · SAREF", 22, GREY).move_to([4.9, 0.9, 0])}
        feeds = []
        for key, t_ in sources.items():
            until(self, v.at(key))
            e = edge(Node(t_[0], t_[0], m.VGroup()), hub, None, dashed=False)
            feeds.append(e)
            self.play(m.FadeIn(t_, shift=0.1 * m.DOWN), grow(e, 0.6), run_time=0.9)
        joint = m.Group(lg, *sources.values(), *feeds, modules)

        # --- a data graph, global and dense
        until(self, v.at("graph"))
        rng = np.random.default_rng(3)
        n = 150
        r = np.sqrt(rng.uniform(0.12, 1, n))
        a = rng.uniform(0, 2 * np.pi, n)
        P = np.column_stack([r * np.cos(a) * 17, r * np.sin(a) * 9.4, np.zeros(n)])
        cats = rng.choice(["execution", "system", "feature", "property", "procedure", "value"], n,
                          p=[0.3, 0.15, 0.2, 0.15, 0.05, 0.15])
        web_nodes = m.VGroup(*[m.Rectangle(width=1.0, height=0.6, fill_color=CAT[c][0], fill_opacity=1,
                                           color=CAT[c][1], stroke_width=4).move_to(p) for p, c in zip(P, cats)])
        links = m.VGroup()
        for i in range(n):
            d = np.linalg.norm(P - P[i], axis=1)
            for j in np.argsort(d)[1:3]:
                links.add(m.Line(P[i], P[j], stroke_width=4, color=LIGHTGREY))
        for x in (*web_nodes, *links):
            x.set_z_index(-3)
        self.play(frame.animate.scale(ZOOM), m.FadeOut(m.VGroup(*sources.values(), *feeds)), m.FadeOut(lg),
                  m.LaggedStart(*[m.Create(l_) for l_ in links], lag_ratio=0.01),
                  m.LaggedStart(*[m.FadeIn(b) for b in web_nodes], lag_ratio=0.01), run_time=3.0)

        until(self, v.at("satellite"))
        uses = ["satellite imagery", "scientific monitoring", "industrial infrastructure", "households",
                "citizen science", "Web of Things"]
        spots = [(-11, 6.0), (9, 6.5), (-13, -1.5), (12, 0.5), (-8, -7.0), (8, -6.5)]
        use_tags = m.VGroup(*[tag(u_, 24 * ZOOM, INK, m.WHITE).move_to([x, y, 0]) for u_, (x, y) in zip(uses, spots)])
        self.play(m.LaggedStart(*[m.FadeIn(t_, scale=0.8) for t_ in use_tags], lag_ratio=0.35), run_time=3.2)

        # --- the 2023 edition: a timeline
        until(self, v.at("first") - 0.3)
        self.play(m.FadeOut(m.Group(web_nodes, links, use_tags, modules)),
                  frame.animate.scale(1 / ZOOM).move_to(m.ORIGIN), run_time=1.2)
        y0 = 0.9
        line = m.Line([-6.4, y0, 0], [-3.2, y0, 0], stroke_width=4, color=GREY)
        stops = {}

        def stop(x: float, year: str, below: list[str]) -> m.VGroup:
            dot = m.Dot([x, y0, 0], radius=0.13, color=HEADING)
            yr = txt(year, 40, HEADING, weight=m.BOLD).next_to(dot, m.UP, buff=0.25)
            lines = m.VGroup(*[txt(b, 22) for b in below]).arrange(m.DOWN, buff=0.1).next_to(dot, m.DOWN, buff=0.3)
            return m.VGroup(dot, yr, lines)

        stops["2017"] = stop(-4.6, "2017", ["SSN", "W3C Recommendation", "OGC Standard"])
        self.play(m.Create(line), run_time=0.6)
        self.play(m.FadeIn(stops["2017"], shift=0.1 * m.UP), run_time=0.8)
        until(self, v.at("iso"))
        stops["iso"] = stop(0.6, "2023", ["ISO 19156:2023", "Observations, measurements", "and samples"])
        self.play(line.animate.put_start_and_end_on([-6.4, y0, 0], [2.4, y0, 0]), run_time=0.8)
        self.play(m.FadeIn(stops["iso"], shift=0.1 * m.UP), run_time=0.8)

        until(self, v.at("edition"))
        stops["ed"] = stop(6.6, "SSN 2023 Edition", [])
        self.play(line.animate.put_start_and_end_on([-6.4, y0, 0], [8.6, y0, 0]), frame.animate.shift(PAN * m.RIGHT),
                  run_time=1.4)
        self.play(m.FadeIn(stops["ed"], shift=0.1 * m.UP), run_time=0.7)
        news = {"canonical": "OMS extension: RDF for ISO 19156", "alignment": "SSN-SAREF alignment",
                "capabilities": "System capabilities module", "humans": "Humans and software as sensors"}
        items = m.VGroup()
        for k, (key, label) in enumerate(news.items()):
            t_ = tag(label, 22).next_to(stops["ed"][0], m.DOWN, buff=0.35 + 0.62 * k)
            t_.align_to([4.5, 0, 0], m.LEFT)
            items.add(t_)
            until(self, v.at(key))
            self.play(m.FadeIn(t_, shift=0.15 * m.LEFT), run_time=0.6)
        until(self, v.at("valid"))
        compat = note_box("Backward compatible", ["2017 data remains valid"], 20)
        compat.move_to([PAN + 4.0, 2.75, 0]).align_to([PAN + 6.9, 0, 0], m.RIGHT)
        self.play(m.FadeIn(compat, shift=0.1 * m.DOWN), run_time=0.8)

        # --- Candidate Recommendation
        until(self, v.at("candidate") - 0.4)
        timeline = m.VGroup(line, *stops.values(), items, compat)
        veil = m.Rectangle(width=40, height=30, stroke_width=0, fill_color=m.WHITE, fill_opacity=0.88).move_to(frame)
        veil.set_z_index(5)
        head = txt("SSN 2023 Edition", 30, GREY)
        cr = txt("W3C Candidate Recommendation", 52, HEADING, weight=m.BOLD)
        stamp_txt = m.VGroup(head, cr).arrange(m.DOWN, buff=0.25)
        stamp_box = m.RoundedRectangle(width=stamp_txt.width + 1.0, height=stamp_txt.height + 0.8, corner_radius=0.2,
                                       color=HEADING, stroke_width=6, fill_color=m.WHITE, fill_opacity=1)
        stamp = m.VGroup(stamp_box, stamp_txt).move_to([PAN, 0.6, 0]).set_z_index(6)
        self.play(m.FadeIn(veil), run_time=0.4)
        self.play(m.FadeIn(stamp, scale=1.5), m.Flash(stamp.get_center(), color=HEADING, line_length=0.6,
                                                     flash_radius=stamp_box.width / 2 + 0.2), run_time=0.9)
        until(self, v.at("implement"))
        call = note_box("Call for implementations",
                        ["Terms marked non-normative become normative",
                         "when evidence of implementation is received.",
                         "Tell us: public-sdw-comments@w3.org"], 24).set_z_index(6)
        self.play(stamp.animate.scale(0.75).move_to([PAN, 2.2, 0]), run_time=0.8)
        call.move_to([PAN, -1.1, 0])
        self.play(m.FadeIn(call, shift=0.1 * m.UP), run_time=0.8)
        until(self, v.at("normative"))
        self.play(m.Indicate(call[2][1], color=HEADING, scale_factor=1.04), run_time=0.9)
        until(self, v.at("tell"))
        self.play(m.Indicate(call[2][3], color=HEADING, scale_factor=1.06), run_time=0.9)

        # --- the series
        until(self, v.at("series"))
        self.play(m.FadeOut(m.Group(timeline, veil, stamp, call)), frame.animate.move_to(m.ORIGIN), run_time=1.0)
        cards = m.VGroup()
        for num, title, place in EPISODES:
            body = m.VGroup(txt(num, 44, HEADING, weight=m.BOLD), txt(title, 24, INK, weight=m.BOLD),
                            txt(place, 20, GREY)).arrange(m.DOWN, buff=0.12)
            bg = m.RoundedRectangle(width=3.05, height=2.25, corner_radius=0.15, fill_color=TOC_BG, fill_opacity=1,
                                    color=RULE, stroke_width=2)
            body.move_to(bg)
            cards.add(m.VGroup(bg, body))
        cards.arrange_in_grid(rows=2, cols=4, buff=(0.3, 0.35)).move_to([0, -0.35, 0])
        heading = txt("The series", 34, HEADING).next_to(cards, m.UP, buff=0.35).align_to(cards, m.LEFT)
        self.play(m.FadeIn(heading), m.LaggedStart(*[m.FadeIn(c_, shift=0.15 * m.UP) for c_ in cards], lag_ratio=0.12),
                  run_time=1.8)
        def light(c_):
            """A highlighted card: blue border, pulsing number (Indicate would tint the whole background)."""
            return m.AnimationGroup(c_[0].animate.set_stroke(HEADING, width=5),
                                    m.Indicate(c_[1][0], color=HEADING, scale_factor=1.25))

        until(self, v.at("vienna"))
        self.play(light(cards[0]), run_time=0.9)
        until(self, v.at("antarctic"))
        self.play(light(cards[1]), run_time=0.9)
        until(self, v.at("more"))
        self.play(m.LaggedStart(*[light(c_) for c_ in cards[2:]], lag_ratio=0.15), run_time=1.6)

        # --- the end
        until(self, v.at("end"))
        self.play(m.FadeOut(m.VGroup(cards, heading, band)), run_time=0.6)
        self.play(m.FadeIn(end_card()), run_time=0.8)
        until(self, v.end + 1.0)
