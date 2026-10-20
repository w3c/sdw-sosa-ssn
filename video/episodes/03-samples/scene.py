"""Episode 3 · SOSA Sampling: an air bubble 7,530 years old.

The voice leads (`v.at(id)`, the `mark`s of episode.yaml). Through video/narrated.sh:

    video/narrated.sh video/episodes/03-samples/episode.yaml --dry     storyboards
    video/narrated.sh video/episodes/03-samples/episode.yaml           MP4

Examples from the spec: ssn/rdf/examples/bubble-provenance.ttl and
paleo-atmosphere.ttl. Real world → model: labelling (A) for the drill, the
core and the bubble; the box that swallows the world (C) for the ice sheet and
the atmosphere.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from globe import Globe  # noqa: E402

SITE = (9.32, -73.35)                # POINT (9.32 -73.35) of ex:WellDrilling4578
VIEW = (9.32, -62.0)                 # the globe, turned towards Antarctica
ICE = "#EAF2F8"                      # the ice, as a pale flat fill
CORE = "#DCEBF5"
SURFACE = 0.6                        # the snow surface, in the cross-section
LAB_Y = -8.6                         # the cutting bench, below the scene (downward pan)

P = {
    "ice": [-4.9, 2.3, 0], "core": [-4.9, -0.25, 0], "bubble": [-4.9, -2.85, 0],
    "drilling": [0.2, 1.05, 0], "coring": [0.2, -1.65, 0],
    "drill": [5.4, 2.4, 0], "person": [4.95, -0.2, 0], "offset": [5.1, -1.75, 0], "atm": [5.0, -3.0, 0],
    "obs_age": [-6.4, -5.4, 0], "obs_co2": [-1.0, -5.4, 0], "obs_atm": [5.0, -5.4, 0],
    "age_p": [-8.0, -7.6, 0], "age_v": [-4.9, -7.6, 0], "co2_p": [-1.5, -7.6, 0], "co2_v": [2.0, -7.6, 0],
    "atm_v": [5.0, -7.6, 0], "atm_t": [8.1, -7.6, 0], "c14": [-6.4, -9.6, 0], "paleo": [5.0, -9.6, 0],
}

TURTLE = """\
ex:Bubble873 a sosa:Sample , sosa:MaterialSample ;
  sosa:isSampleOf ex:IceCore12 , ex:EarthAtmosphere ;
  sosa:isSampleOfUltimateFOI ex:Antarctic_ice_sheet ;
  sosa:isResultOf ex:CoreEx1923 ."""


# ------------------------------------------------------------- the real world, line-drawn
def ice_section() -> m.VGroup:
    """The ice-sheet cross-section: the ice, its annual layers, the surface."""
    body = m.Rectangle(width=14.4, height=SURFACE + 3.7, stroke_width=0, fill_color=ICE, fill_opacity=1)
    body.align_to([0, SURFACE, 0], m.UP)
    layers = m.VGroup()
    for k, y in enumerate(np.linspace(SURFACE - 0.6, -3.4, 7)):
        xs = np.linspace(-7.2, 7.2, 60)
        pts = [[x, y + 0.06 * np.sin(1.3 * x + k), 0] for x in xs]
        layers.add(m.VMobject(stroke_width=1.5, color="#C3D5E4").set_points_smoothly(pts))
    surf = m.Line([-7.2, SURFACE, 0], [7.2, SURFACE, 0], stroke_width=3, color=GREY)
    return m.VGroup(body, layers, surf)


def tower(x: float = 5.4) -> m.VGroup:
    """The thermal drill: a tripod, a winch."""
    s = dict(stroke_width=3, color=INK)
    top = [x, SURFACE + 2.5, 0]
    legs = m.VGroup(m.Line([x - 0.7, SURFACE, 0], top, **s), m.Line([x + 0.7, SURFACE, 0], top, **s),
                    m.Line([x - 0.35, SURFACE + 1.25, 0], [x + 0.35, SURFACE + 1.25, 0], **s))
    winch = m.Rectangle(width=0.55, height=0.4, fill_color="#E6E6E6", fill_opacity=1, **s)
    winch.move_to([x + 1.0, SURFACE + 0.2, 0])
    pulley = m.Circle(radius=0.12, fill_color=m.WHITE, fill_opacity=1, **s).move_to(top)
    return m.VGroup(legs, winch, pulley)


def core_v(height: float = 2.4) -> m.VGroup:
    body = m.RoundedRectangle(width=0.34, height=height, corner_radius=0.08, stroke_width=2.5, color=INK,
                              fill_color=CORE, fill_opacity=1)
    rings = m.VGroup(*[m.Line(body.get_left() + [0.04, dy, 0], body.get_right() + [-0.04, dy, 0], stroke_width=1,
                              color="#9DB7CC") for dy in np.linspace(-height / 2 + 0.3, height / 2 - 0.3, 6)])
    return m.VGroup(body, rings)


class Episode03(m.Scene):
    def link(self, a, b, name, nodes, **kw) -> Edge:
        """An arrow whose label avoids the nodes and the labels already placed;
        its own is added to the list."""
        e = edge(a, b, name, avoid=nodes, size=21, **kw)
        if e.label is not None:
            nodes.append(e.label)
        return e

    def construct(self) -> None:
        v = Voice()
        frame = self.camera.frame

        # --- the title card
        card = title_card("Episode 3 · Samples", "The SOSA Sampling module")
        self.add(card)
        until(self, v.at("globe") - 0.7)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the globe, towards Antarctica
        g = Globe(3.4)
        lon, lat = m.ValueTracker(-20), m.ValueTracker(25)
        world = m.always_redraw(lambda: g.draw(lon.get_value(), lat.get_value()))
        self.play(m.FadeIn(world), lon.animate.set_value(0), run_time=2.0, rate_func=m.linear)
        until(self, v.at("antarctica") - 1.2)
        self.play(lon.animate.set_value(VIEW[0]), lat.animate.set_value(VIEW[1]), run_time=2.6)
        world.clear_updaters()
        self.remove(world)
        fine = Globe(3.4, detail="50m").draw(*VIEW)
        self.add(fine)

        until(self, v.at("april"))
        here = g.point(*VIEW, *SITE)
        site = m.Dot(here, radius=0.08, color=HEADING)
        self.play(m.FadeIn(site, scale=3), m.Flash(here, color=HEADING, line_length=0.15), run_time=0.8)
        self.play(fine.animate.scale(4.5, about_point=here), run_time=1.6)

        # --- the drilling
        ice = ice_section()
        drill = tower()
        depth = m.ValueTracker(SURFACE)
        hole = m.always_redraw(lambda: m.Rectangle(width=0.36, height=max(SURFACE - depth.get_value(), 0.01),
                                                   stroke_width=1.5, color=GREY, fill_color=m.WHITE, fill_opacity=1)
                               .move_to([5.4, (SURFACE + depth.get_value()) / 2, 0]))
        cable = m.always_redraw(lambda: m.Line([5.4, SURFACE + 2.5, 0], [5.4, depth.get_value(), 0],
                                               stroke_width=1.5, color=INK))
        head = m.always_redraw(lambda: m.Rectangle(width=0.22, height=0.4, stroke_width=0, fill_color=GREY,
                                                   fill_opacity=1).move_to([5.4, depth.get_value() - 0.2, 0]))
        stamp = txt("3 April 2017 · 73.35° S, 9.32° E", 26, GREY).to_corner(m.UR, buff=0.45)
        until(self, v.at("bores"))
        self.play(m.FadeOut(m.VGroup(fine, site)), run_time=0.6)
        self.play(m.FadeIn(ice), m.Create(drill, lag_ratio=0.2), m.FadeIn(stamp), run_time=1.2)
        self.add(hole, cable, head)
        self.play(depth.animate.set_value(-2.8), run_time=2.0, rate_func=m.linear)
        until(self, v.at("south"))
        self.play(m.Indicate(stamp, color=HEADING, scale_factor=1.05), run_time=0.8)

        until(self, v.at("core"))
        core = core_v().move_to([5.4, -1.6, 0])
        self.add(core)
        self.bring_to_front(cable, head)
        self.play(depth.animate.set_value(SURFACE + 0.3), core.animate.move_to([5.4, SURFACE + 1.2, 0]), run_time=1.4)
        self.play(core.animate.move_to([3.0, -0.8, 0]), run_time=0.7)

        # --- from the real world to the model: the first sampling
        band = hud("SOSA · Sampling module")
        until(self, v.at("feature"))
        hole.clear_updaters()
        cable.clear_updaters()
        head.clear_updaters()
        thumb = m.VGroup(ice, hole).copy().set(height=0.5)
        ice_n = ind("ex:Antarctic_ice_sheet", "feature", size=22, icon=thumb).move_to(P["ice"])
        self.play(m.FadeIn(band), m.FadeOut(stamp), m.FadeOut(m.VGroup(cable, head)),
                  m.FadeIn(ice_n.box), m.Create(ice_n.border),
                  m.ReplacementTransform(m.VGroup(ice, hole), ice_n.label[0]), m.FadeIn(ice_n.label[1]), run_time=1.6)
        pin(self, band)

        nodes = [ice_n]
        until(self, v.at("sampling"))
        drilling = ind("ex:WellDrilling4578", "execution", size=22, sub="drilling").move_to(P["drilling"])
        e1 = self.link(drilling, ice_n, "hasFeatureOfInterest", nodes)
        self.play(appear(drilling, 0.8))
        self.play(grow(e1))
        nodes.append(drilling)

        until(self, v.at("sampler"))
        drill_n = ind("ex:ThermalDrill2", "system", size=22, sub="thermal drill").move_to(P["drill"])
        ring = m.DashedVMobject(m.Rectangle(width=2.6, height=3.0, color=CAT["system"][1], stroke_width=3),
                                num_dashes=60).move_to(drill)
        self.play(m.Create(ring), run_time=0.6)
        self.play(m.FadeIn(drill_n.box), m.ReplacementTransform(ring, drill_n.border),
                  m.ReplacementTransform(drill, drill_n.label), run_time=1.1)
        e2 = self.link(drilling, drill_n, "madeBySampler", nodes)
        self.play(grow(e2))
        nodes.append(drill_n)

        until(self, v.at("sample"))
        core_n = ind("ex:IceCore12", "feature", size=22, sub="ice core").move_to(P["core"])
        ring = m.DashedVMobject(m.Rectangle(width=0.8, height=2.8, color=CAT["feature"][1], stroke_width=3),
                                num_dashes=40).move_to(core)
        self.play(m.Create(ring), run_time=0.5)
        self.play(m.FadeIn(core_n.box), m.ReplacementTransform(ring, core_n.border),
                  m.ReplacementTransform(core, core_n.label), run_time=1.2)
        e3 = self.link(drilling, core_n, "hasResult", nodes, side=-1)
        self.play(grow(e3))
        nodes.append(core_n)
        until(self, v.at("represent"))
        e4 = self.link(core_n, ice_n, "isSampleOf", nodes)
        self.play(grow(e4), m.Indicate(ice_n, scale_factor=1.04, color=CAT["feature"][1]))

        # --- downward pan: the cutting, the bubble
        until(self, v.at("january"))
        L = 9.6                                     # 20 m of core
        x0 = -L / 2
        bar = m.VGroup(*[m.RoundedRectangle(width=L / 4 - 0.06, height=0.5, corner_radius=0.08, stroke_width=2.5,
                                            color=INK, fill_color=CORE, fill_opacity=1)
                         .move_to([x0 + L / 8 + k * L / 4, LAB_Y + 2.2, 0]) for k in range(4)])
        ticks = m.VGroup()
        for d in range(0, 21, 5):
            x = x0 + d * L / 20
            ticks.add(m.Line([x, LAB_Y + 1.85, 0], [x, LAB_Y + 1.7, 0], stroke_width=2, color=GREY),
                      txt(f"{d} m", 20, GREY).move_to([x, LAB_Y + 1.45, 0]))
        when = txt("9 January 2018", 26, GREY).move_to([0, LAB_Y + 3.2, 0])
        self.play(frame.animate.move_to([0, LAB_Y, 0]), run_time=1.6)
        self.play(m.FadeIn(bar, lag_ratio=0.2), m.FadeIn(ticks), m.FadeIn(when), run_time=1.0)

        until(self, v.at("metres"))
        xc = x0 + 15.202 * L / 20
        cut = m.DashedLine([xc, LAB_Y + 2.7, 0], [xc, LAB_Y + 1.7, 0], color=HEADING, stroke_width=4)
        cut_t = txt("15.202 m", 24, HEADING).next_to(cut, m.UP, buff=0.1)
        self.play(m.Create(cut), m.FadeIn(cut_t), run_time=0.8)
        slab = m.RoundedRectangle(width=4.2, height=2.6, corner_radius=0.15, stroke_width=2.5, color=INK,
                                  fill_color=CORE, fill_opacity=1).move_to([0, LAB_Y - 1.1, 0])
        rng = np.random.default_rng(11)
        bubbles = m.VGroup()
        for _ in range(16):
            r = rng.uniform(0.05, 0.13)
            bubbles.add(m.Circle(radius=r, stroke_width=1.6, color="#7F9AB0", fill_color=m.WHITE, fill_opacity=0.9)
                        .move_to(slab.get_center() + [rng.uniform(-1.8, 1.8), rng.uniform(-1.05, 1.05), 0]))
        the = m.Circle(radius=0.14, stroke_width=2, color="#7F9AB0", fill_color=m.WHITE, fill_opacity=1)
        the.move_to(slab.get_center() + [0.4, 0.15, 0])
        self.play(m.GrowFromPoint(m.VGroup(slab, bubbles, the), [xc, LAB_Y + 2.2, 0]), run_time=1.2)

        until(self, v.at("bubble"))
        glow = m.Circle(radius=0.3, color=HEADING, stroke_width=4).move_to(the)
        self.play(the.animate.scale(2.2), m.Create(glow), m.Flash(the.get_center(), color=HEADING), run_time=1.0)

        # --- the second sampling
        until(self, v.at("second"))
        bubble_n = ind("ex:Bubble873", "feature", size=22, sub="a bubble of air").move_to(P["bubble"])
        coring = ind("ex:CoreEx1923", "execution", size=22, sub="cutting the core").move_to(P["coring"])
        lab = m.VGroup(bar, ticks, when, cut, cut_t, slab, bubbles)
        self.play(frame.animate.move_to(m.ORIGIN), m.FadeOut(lab), m.FadeOut(glow),
                  m.ReplacementTransform(the, bubble_n.label[0]), m.FadeIn(bubble_n.box), m.Create(bubble_n.border),
                  m.FadeIn(bubble_n.label[1]), run_time=1.8)
        nodes.append(bubble_n)
        e5 = self.link(coring, core_n, "hasFeatureOfInterest", nodes)
        self.play(appear(coring, 0.7), grow(e5), run_time=1.0)
        nodes.append(coring)

        until(self, v.at("person"))
        person = ind("orcid:0000-0002-3884-3420", "system", size=16, sub="a person").move_to(P["person"])
        e6 = self.link(coring, person, "madeBySampler", nodes, side=1, label_pos=0.42)
        self.play(grow(e6), appear(person, 0.8), run_time=1.0)
        nodes.append(person)
        until(self, v.at("depth"))
        offset = value("offset · 15.202 m", 22).move_to(P["offset"])
        e7 = self.link(coring, offset, "hasInputValue", nodes, side=-1)
        self.play(grow(e7), appear(offset, 0.8), run_time=1.0)
        nodes.append(offset)
        until(self, v.at("result"))
        e8 = self.link(coring, bubble_n, "hasResult", nodes, side=-1)
        self.play(grow(e8))

        # --- the bubble: a sample of the core, and of the atmosphere
        until(self, v.at("ofcore"))
        e9 = self.link(bubble_n, core_n, "isSampleOf", nodes)
        self.play(grow(e9))
        until(self, v.at("atmosphere"))
        mini = Globe(0.75, center=P["atm"]).draw(10, 30, stroke=1.2)
        halo = m.Circle(radius=0.86, stroke_width=9, color=HEADING, stroke_opacity=0.35).move_to(P["atm"])
        self.play(m.FadeIn(mini, scale=0.8), m.Create(halo), run_time=0.8)
        atm = ind("ex:EarthAtmosphere", "feature", size=22, icon=m.VGroup(mini, halo).copy().set(height=0.7)).move_to(P["atm"])
        self.play(m.FadeIn(atm.box), m.Create(atm.border), m.ReplacementTransform(m.VGroup(mini, halo), atm.label[0]),
                  m.FadeIn(atm.label[1]), run_time=1.2)
        nodes.append(atm)
        e10 = self.link(bubble_n, atm, "isSampleOf", nodes)
        self.play(grow(e10))

        # --- at the end of the chain: the ice sheet
        until(self, v.at("ultimate"))
        self.play(frame.animate.set(width=18).move_to([-0.8, -0.2, 0]), m.FadeOut(band), run_time=1.2)
        a = bubble_n.box.get_left() + 0.04 * m.LEFT
        b = ice_n.box.get_left() + 0.04 * m.LEFT
        arc = m.ArcBetweenPoints(a, b, angle=-1.1, color="#333333", stroke_width=3)
        ult = m.DashedVMobject(arc, num_dashes=40)
        tip = m.Arrow(arc.point_from_proportion(0.97), b, buff=0, stroke_width=3, color="#333333",
                      tip_shape=m.StealthTip, max_tip_length_to_length_ratio=0.9)
        tip.set_stroke(opacity=0)
        tip.tip.set_stroke(opacity=1)
        ult_t = txt("isSampleOfUltimateFOI", 24, "#333333", slant=m.ITALIC).rotate(np.pi / 2)
        ult_t.next_to(arc, m.LEFT, buff=0.12)
        self.play(m.Create(ult), m.GrowArrow(tip), run_time=1.4)
        self.play(m.FadeIn(ult_t), m.Indicate(ice_n, scale_factor=1.04, color=CAT["feature"][1]), run_time=0.9)
        ultimate = m.VGroup(ult, tip, ult_t)

        # --- the observations, further down
        until(self, v.at("two"))
        self.play(frame.animate.set(width=19.5).move_to([0, -6.0, 0]), run_time=1.4)
        obs_co2 = ind("ex:Ob873c4", "execution", size=22, sub="an observation").move_to(P["obs_co2"])
        obs_age = ind("ex:Ob873t2", "execution", size=22, sub="an observation").move_to(P["obs_age"])
        co2_p = ind("ex:CO2-Concentration", "property", size=22).move_to(P["co2_p"])
        co2_v = value("240 ppm", 22).move_to(P["co2_v"])
        age_p = ind("ex:Age-of-Air", "property", size=22).move_to(P["age_p"])
        age_v = value("7530 yr", 22).move_to(P["age_v"])
        c14 = ind("ex:C14-Age", "procedure", size=22, sub="radiocarbon dating").move_to(P["c14"])
        low = [obs_co2, obs_age, co2_p, co2_v, age_p, age_v, c14]
        nodes += low
        # no label: hasFeatureOfInterest is already named three times above, and the arc of the
        # second hasInputValue passes through here
        o1 = edge(obs_co2, bubble_n, None)
        o2 = edge(obs_age, bubble_n, None)
        self.play(appear(obs_co2, 0.7), appear(obs_age, 0.7), run_time=0.9)
        self.play(grow(o1), grow(o2), run_time=0.9)
        until(self, v.at("carbon"))
        o3 = self.link(obs_co2, co2_p, "observedProperty", nodes)
        o4 = self.link(obs_co2, co2_v, "hasResult", nodes, side=-1)
        self.play(grow(o3), appear(co2_p, 0.6), run_time=0.9)
        self.play(grow(o4), appear(co2_v, 0.6), run_time=0.9)
        until(self, v.at("age"))
        o5 = self.link(obs_age, age_p, "observedProperty", nodes)
        o6 = self.link(obs_age, age_v, "hasResult", nodes, side=-1)
        self.play(grow(o5), appear(age_p, 0.6), run_time=0.9)
        self.play(grow(o6), appear(age_v, 0.6), run_time=0.9)
        until(self, v.at("radiocarbon"))
        o7 = self.link(obs_age, c14, "usedProcedure", nodes)
        self.play(grow(o7), appear(c14, 0.7), run_time=1.0)

        until(self, v.at("together"))
        obs_atm = ind("ex:Oatc349", "execution", size=22, sub="an observation").move_to(P["obs_atm"])
        nodes.append(obs_atm)
        i1 = self.link(obs_atm, obs_co2, "hasInputValue", nodes)
        arc2 = m.ArcBetweenPoints(obs_atm.box.get_top() + 0.6 * m.LEFT, obs_age.box.get_top() + 0.4 * m.RIGHT,
                                  angle=1.0, color="#333333", stroke_width=3)
        i2 = m.DashedVMobject(arc2, num_dashes=60)
        tip2 = m.Arrow(arc2.point_from_proportion(0.96), arc2.get_end(), buff=0, stroke_width=3, color="#333333",
                       tip_shape=m.StealthTip, max_tip_length_to_length_ratio=0.9)
        tip2.set_stroke(opacity=0)
        tip2.tip.set_stroke(opacity=1)
        self.play(appear(obs_atm, 0.8))
        self.play(grow(i1), m.Create(i2), m.GrowArrow(tip2), run_time=1.2)
        until(self, v.at("itself"))
        o8 = self.link(obs_atm, atm, "hasFeatureOfInterest", nodes)
        atm_v = value("240 ppm", 22).move_to(P["atm_v"])
        nodes.append(atm_v)
        o9 = self.link(obs_atm, atm_v, "hasResult", nodes, side=-1)
        self.play(grow(o8), run_time=0.8)
        self.play(grow(o9), appear(atm_v, 0.6), run_time=0.9)
        until(self, v.at("before"))
        atm_t = value("7530 BP", 24).move_to(P["atm_t"])
        paleo = ind("ex:P-paleo-CO2", "procedure", size=22).move_to(P["paleo"])
        o10 = self.link(obs_atm, atm_t, "phenomenonTime", nodes)
        o11 = self.link(obs_atm, paleo, "usedProcedure", nodes, side=-1)
        self.play(grow(o10), appear(atm_t, 0.6), run_time=0.9)
        self.play(grow(o11), appear(paleo, 0.6), run_time=0.9)

        # --- the whole chain
        graph = m.VGroup(ice_n, core_n, bubble_n, drilling, coring, drill_n, person, offset, atm, *low, obs_atm,
                         atm_v, atm_t, paleo, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, ultimate,
                         o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, i1, i2, tip2)
        until(self, v.at("chain"))
        self.play(frame.animate.set(width=graph.width + 1.2).move_to(graph.get_center()), run_time=1.6)
        until(self, v.at("link"))
        chain = [e4, e9, e10, o1, o2, o8]
        self.play(m.LaggedStart(*[m.ShowPassingFlash(e.tip_line.copy().set_stroke(HEADING, width=10, opacity=1),
                                                     time_width=0.6) for e in chain], lag_ratio=0.2),
                  m.ShowPassingFlash(ult.copy().set_stroke(HEADING, width=10), time_width=0.6), run_time=1.8)

        # --- the classes of the Sampling module
        until(self, v.at("classes"))
        self.play(m.FadeOut(graph), frame.animate.set(width=m.config.frame_width).move_to(m.ORIGIN), m.FadeIn(band),
                  run_time=1.2)
        C = {"exe": cls("Execution", 26, context=True).move_to([0, 2.7, 0]),
             "sampling": cls("Sampling", 26).move_to([0, 0.7, 0]),
             "sampler": cls("Sampler", 26).move_to([-4.9, 0.7, 0]),
             "proc": cls("SamplingProcedure", 26).move_to([-4.6, -2.3, 0]),
             "foi": cls("FeatureOfInterest", 26).move_to([4.6, 2.5, 0]),
             "sample": cls("Sample", 26).move_to([4.6, -1.9, 0])}
        taken = list(C.values())
        CE = [edge(C["sampling"], C["exe"], None, dashed=False, open_tip=True)]
        for a_, b_, name, sd in (("sampling", "sampler", "madeBySampler", 1), ("sampling", "proc", "usedProcedure", -1),
                                 ("sampler", "proc", "implements", 1), ("sampling", "foi", "hasFeatureOfInterest", 1),
                                 ("sampling", "sample", "hasResult", -1), ("sample", "foi", "isSampleOf", -1)):
            CE.append(edge(C[a_], C[b_], name, dashed=False, side=sd, size=22, avoid=taken))
            taken.append(CE[-1].label)
        self.play(m.LaggedStart(*[appear(n, 0.5) for n in C.values()], lag_ratio=0.12), run_time=1.0)
        self.play(m.LaggedStart(*[grow(e, 0.5) for e in CE], lag_ratio=0.12), run_time=1.3)
        model = m.VGroup(*C.values(), *CE)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · bubble-provenance.ttl", 22)
        ex.set(width=min(ex.width, 13.0)).move_to(0.1 * m.DOWN)
        self.play(m.FadeOut(model), m.FadeIn(ex, shift=0.2 * m.UP), run_time=1.0)
        until(self, v.at("lines"))
        for i in range(4):
            self.play(ex.line(i).animate.set_color(HEADING), run_time=0.3)

        # --- the end
        until(self, v.at("module"))
        self.play(m.FadeOut(ex), m.FadeOut(band), run_time=0.6)
        self.play(m.FadeIn(end_card()), run_time=0.8)
        until(self, v.at("tuned"))
        more = txt("Stay tuned for more", 30, HEADING).to_edge(m.DOWN, buff=0.7)
        self.play(m.FadeIn(more, shift=0.1 * m.UP))
        until(self, v.end + 1.0)
