"""Episode 2 · SOSA Observation: Vienna, 4 April 1872 at 3 pm.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/02-observation/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/02-observation/episode.yaml           MP4

Example from the spec: ssn/rdf/examples/historical-airtemp.ttl. From the real
world to the model (video/scenarios.md): labelling (A) for the thermometer and
the value, the box that swallows the world (C) for the station and the atmosphere.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from globe import Globe  # noqa: E402

VIENNA = (16.3558, 48.2485)
VIEW = (16.36, 42.0)                 # the centre of the globe when looking at Vienna
MERCURY = "#7F8C99"

# The graph, in scene units (14.2 x 8 frame)
P = {
    "obs": m.UP * 0.2,
    "t99": m.LEFT * 5.0 + m.UP * 2.5,
    "shw": m.LEFT * 5.0 + m.DOWN * 1.6,
    "air": m.RIGHT * 5.0 + m.UP * 2.5,
    "val": m.RIGHT * 5.0 + m.DOWN * 1.2,
    "time": m.DOWN * 2.8 + m.RIGHT * 0.4,
    "atm": m.RIGHT * 11.6 + m.UP * 2.5,
}
PAN = 6.6                            # the pan towards the atmosphere

TURTLE = """\
ex:SHW_T_1872-04-04T15 a sosa:Observation ;
  sosa:madeBySensor ex:T99 ;
  sosa:observedProperty ex:airTemperature ;
  sosa:hasFeatureOfInterest ex:SHW ;
  sosa:phenomenonTime [
    time:inXSDDateTime "1872-04-04T15:00:00+01:00"^^xsd:dateTime ] ;
  sosa:hasResult [ qudt:value 22.5 ; qudt:hasUnit unit:DEG_C ] .

ex:SHW a sosa:Platform , sosa:FeatureOfInterest ;
  sosa:hosts ex:T99 .
ex:airTemperature a sosa:Property ;
  sosa:isPropertyOf ex:EarthAtmosphere ."""


# ------------------------------------------------------------- the real world, line-drawn
def station() -> m.VGroup:
    """The Hohe Warte station: the tower building, the weather shelter."""
    s = dict(stroke_width=2.5, color=INK)
    base = -2.6
    body = m.Rectangle(width=4.2, height=1.7, fill_color="#FAFAFA", fill_opacity=1, **s)
    body.move_to([-3.8, base + 0.85, 0])
    tower = m.Rectangle(width=1.0, height=1.0, fill_color="#FAFAFA", fill_opacity=1, **s)
    tower.next_to(body, m.UP, buff=0)
    roof = m.Polygon(tower.get_corner(m.UL) + 0.1 * m.LEFT, tower.get_corner(m.UR) + 0.1 * m.RIGHT,
                     tower.get_top() + 0.55 * m.UP, fill_color="#E6E6E6", fill_opacity=1, **s)
    cornice = m.Line(body.get_corner(m.UL) + 0.12 * m.LEFT, body.get_corner(m.UR) + 0.12 * m.RIGHT, **s)
    windows = m.VGroup(*[
        m.Rectangle(width=0.26, height=0.4, stroke_width=1.6, color=INK).move_to([x, y, 0])
        for y in (base + 0.45, base + 1.2) for x in np.linspace(-5.5, -2.1, 7) if abs(x + 3.8) > 0.2
    ])
    door = m.Rectangle(width=0.42, height=0.72, stroke_width=2, color=INK).move_to([-3.8, base + 0.36, 0])
    tw = m.Rectangle(width=0.24, height=0.36, stroke_width=1.6, color=INK).move_to(tower)
    building = m.VGroup(body, tower, roof, cornice, windows, door, tw)

    legs = m.VGroup(*[m.Line([x, base, 0], [x, base + 1.1, 0], **s) for x in (0.42, 1.18)])
    box = m.Rectangle(width=0.9, height=0.75, fill_color=m.WHITE, fill_opacity=1, **s)
    box.move_to([0.8, base + 1.1 + 0.375, 0])
    louvres = m.VGroup(*[m.Line(box.get_left() + [0.08, dy, 0], box.get_right() + [-0.08, dy, 0],
                                stroke_width=1.2, color=GREY) for dy in np.linspace(-0.25, 0.25, 5)])
    hat = m.Polygon(box.get_corner(m.UL) + 0.12 * m.LEFT, box.get_corner(m.UR) + 0.12 * m.RIGHT,
                    box.get_top() + 0.25 * m.UP, fill_color="#E6E6E6", fill_opacity=1, **s)
    shelter = m.VGroup(legs, box, louvres, hat)

    ground = m.Line([-6.6, base, 0], [2.4, base, 0], stroke_width=2, color=GREY)
    return m.VGroup(ground, building, shelter)


def thermometer(level: m.ValueTracker, center) -> tuple[m.VGroup, m.VMobject, callable]:
    """The mercury thermometer, its scale and its column (which follows `level`, in °C)."""
    c = np.asarray(center, float)
    tube = m.RoundedRectangle(width=0.32, height=3.3, corner_radius=0.16, stroke_width=2.5, color=INK,
                              fill_color=m.WHITE, fill_opacity=1).move_to(c + 0.2 * m.UP)
    bulb = m.Circle(radius=0.3, stroke_width=2.5, color=INK, fill_color=MERCURY, fill_opacity=1)
    bulb.move_to(tube.get_bottom() + 0.12 * m.DOWN)
    y0, y1 = tube.get_bottom()[1] + 0.2, tube.get_top()[1] - 0.25

    def y_of(t: float) -> float:
        return y0 + (t + 10) / 50 * (y1 - y0)

    ticks = m.VGroup()
    for t in range(-10, 41, 5):
        major = t % 10 == 0
        x = tube.get_right()[0]
        ticks.add(m.Line([x + 0.05, y_of(t), 0], [x + (0.3 if major else 0.18), y_of(t), 0],
                         stroke_width=1.6, color=INK))
        if major:
            ticks.add(txt(str(t), 20, GREY).move_to([x + 0.6, y_of(t), 0]))
    unit = txt("°C", 20, GREY).next_to(tube, m.UP, buff=0.15).shift(0.45 * m.RIGHT)
    column = m.always_redraw(lambda: m.Rectangle(
        width=0.13, height=max(y_of(level.get_value()) - (y0 - 0.25), 0.01), stroke_width=0,
        fill_color=MERCURY, fill_opacity=1).align_to([c[0], y0 - 0.25, 0], m.DOWN).set_x(tube.get_x()))
    return m.VGroup(tube, ticks, unit, bulb), column, y_of


# ------------------------------------------------------------- the scene
class Episode02(m.Scene):
    def construct(self) -> None:
        v = Voice()
        frame = self.camera.frame

        # --- the title card
        card = title_card("Episode 2 · Observations", "The SOSA Observation module")
        self.add(card)
        until(self, v.at("globe") - 0.7)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the planet, and its sensors
        g = Globe(3.4)
        lon, lat, dots = m.ValueTracker(-35), m.ValueTracker(12), m.ValueTracker(0)
        rng = np.random.default_rng(7)
        z = rng.uniform(-1, 1, 500)
        sens = np.column_stack([rng.uniform(-180, 180, 500), np.degrees(np.arcsin(z))])

        def earth():
            l0, p0 = lon.get_value(), lat.get_value()
            out = g.draw(l0, p0)
            if dots.get_value() > 0.01:
                xy, cosc = __import__("globe").ortho(np.radians(sens), l0, p0)
                pts = g.to_scene(xy[cosc > 0.05])
                out.add(m.VGroup(*[m.Dot(p, radius=0.035, color=CAT["system"][1], fill_opacity=dots.get_value())
                                   for p in pts]))
            return out

        world = m.always_redraw(earth)
        self.play(m.FadeIn(world), lon.animate.set_value(-20), run_time=1.5, rate_func=m.linear)
        until(self, v.at("sensors"))
        self.play(dots.animate.set_value(1), lon.animate.set_value(-5), run_time=2.5, rate_func=m.linear)
        until(self, v.at("one"))
        self.play(lon.animate.set_value(VIEW[0]), lat.animate.set_value(VIEW[1]), dots.animate.set_value(0),
                  run_time=3)
        world.clear_updaters()
        self.remove(world)
        fine = Globe(3.4, detail="50m", borders=True).draw(*VIEW)
        here = g.point(*VIEW, *VIENNA)
        self.add(fine)
        pin_dot = m.Dot(here, radius=0.07, color=HEADING)
        self.play(m.FadeIn(pin_dot, scale=3), m.Flash(here, color=HEADING, line_length=0.15), run_time=0.8)

        until(self, v.at("vienna"))
        name = txt("Vienna", 30, HEADING).next_to(here, m.UR, buff=0.15)
        name = m.VGroup(m.BackgroundRectangle(name, color=m.WHITE, fill_opacity=0.85, buff=0.08), name)
        self.play(fine.animate.scale(14, about_point=here), m.FadeIn(name), run_time=2.5)
        self.play(m.FadeOut(m.VGroup(fine, pin_dot, name)), run_time=0.6)

        # --- the station
        st = station()
        ground, building, shelter = st
        place = txt("Hohe Warte, Vienna", 22, GREY).move_to([-3.8, -3.05, 0])
        until(self, v.at("station"))
        self.play(m.Create(ground), m.Create(building, lag_ratio=0.1), m.FadeIn(place), run_time=1.8)
        until(self, v.at("shelter"))
        self.play(m.Create(shelter, lag_ratio=0.2), run_time=1.2)
        lens = m.Circle(radius=2.5, stroke_width=2, color=GREY, fill_color=m.WHITE, fill_opacity=1)
        lens.move_to([4.4, 0.4, 0])
        box = shelter[1]
        rays = m.VGroup(m.Line(box.get_corner(m.UR), lens.point_at_angle(np.radians(160)), stroke_width=1.5, color=GREY),
                        m.Line(box.get_corner(m.DR), lens.point_at_angle(np.radians(235)), stroke_width=1.5, color=GREY))
        level = m.ValueTracker(9)
        therm, column, y_of = thermometer(level, [4.0, 0.3, 0])
        # once a graph box (z-index 1 to 3) is on stage, ordering follows the z-index: so we set it
        # for the magnifier and its contents too
        lens.set_z_index(0.1)
        therm.set_z_index(0.2)
        column.set_z_index(0.3)
        self.play(m.Create(rays), m.GrowFromPoint(lens, box.get_center()), run_time=0.9)
        self.play(m.FadeIn(therm), m.FadeIn(column), run_time=0.7)

        until(self, v.at("date"))
        date = txt("4 April 1872 · 15:00", 30, GREY).move_to(P["time"] + 0.35 * m.DOWN)
        self.play(m.FadeIn(date, shift=0.1 * m.DOWN))
        until(self, v.at("reads"))
        self.play(level.animate.set_value(22.5), run_time=1.8)
        reading = txt("22.5 °C", 30, INK).move_to([2.66, y_of(22.5), 0]).set_z_index(0.5)
        until(self, v.at("celsius"))
        self.play(m.Write(reading), run_time=0.7)

        # --- from the real world to the model
        band = hud("SOSA · Observation module")
        until(self, v.at("identifier"))
        iri = mono("https://example.org/data/T99", 22).next_to(lens, m.UP, buff=0.15)
        self.play(m.FadeIn(band), m.Write(iri), run_time=1.0)
        pin(self, band)

        # A: the thermometer gets an orange dashed outline, its name shortens
        until(self, v.at("thermometer"))
        t99 = ind("ex:T99", "system", sub="mercury thermometer").move_to(P["t99"])
        ring = m.DashedVMobject(m.Rectangle(width=1.75, height=4.5, color=CAT["system"][1], stroke_width=3),
                                num_dashes=70, dashed_ratio=0.45).move_to(therm.get_center()).set_z_index(0.5)
        short = mono("ex:T99", 24).next_to(ring, m.UP, buff=0.1)
        short.add_background_rectangle(color=m.WHITE, opacity=1, buff=0.06)
        short.set_z_index(0.5)
        self.play(m.Create(ring), m.TransformMatchingShapes(iri, short), run_time=1.0)

        # C: the station shrinks into its yellow box
        until(self, v.at("thestation"))
        thumb = m.VGroup(building, shelter).copy().set(height=0.9)
        shw = ind("ex:SHW", "feature", sub="Station Hohe Warte", icon=thumb).move_to(P["shw"])
        self.play(m.FadeOut(rays), m.FadeOut(place), m.FadeOut(ground),
                  m.FadeIn(shw.box), m.Create(shw.border),
                  m.ReplacementTransform(m.VGroup(building, shelter), shw.label[0]),
                  m.FadeIn(shw.label[1]), run_time=1.6)

        # A: the reading becomes a value, the thermometer becomes its node
        until(self, v.at("value"))
        val = value("22.5 °C").move_to(P["val"])
        self.play(m.FadeOut(m.VGroup(lens, therm)), m.FadeOut(column),
                  m.FadeIn(val.box), m.Create(val.border), m.ReplacementTransform(reading, val.label),
                  m.FadeIn(t99.box), m.ReplacementTransform(ring, t99.border),
                  m.ReplacementTransform(short, t99.label[0]), m.FadeIn(t99.label[1]), run_time=1.6)

        # --- the graph builds up
        until(self, v.at("observation"))
        obs = ind("ex:SHW_T_1872-04-04T15", "execution", sub="an observation").move_to(P["obs"])
        air = ind("ex:airTemperature", "property").move_to(P["air"])
        tim = value("1872-04-04T15:00+01:00", 22).move_to(P["time"])
        nodes = [obs, t99, shw, air, val, tim]
        self.play(appear(obs, 1.0))

        until(self, v.at("made"))
        e_sensor = edge(obs, t99, "madeBySensor", side=-1, avoid=nodes)
        nodes.append(e_sensor.label)
        self.play(grow(e_sensor))
        until(self, v.at("observed"))
        e_prop = edge(obs, air, "observedProperty", avoid=nodes)
        nodes.append(e_prop.label)
        self.play(grow(e_prop))
        self.play(appear(air, 0.7))
        until(self, v.at("interest"))
        e_foi = edge(obs, shw, "hasFeatureOfInterest", side=-1, avoid=nodes)
        nodes.append(e_foi.label)
        self.play(grow(e_foi), m.Indicate(shw, scale_factor=1.05, color=CAT["feature"][1]))

        until(self, v.at("result"))
        e_res = edge(obs, val, "hasResult", avoid=nodes)
        nodes.append(e_res.label)
        self.play(grow(e_res))
        until(self, v.at("time"))
        e_time = edge(obs, tim, "phenomenonTime", side=1, avoid=nodes)
        nodes.append(e_time.label)
        self.play(grow(e_time), m.FadeIn(tim.box), m.Create(tim.border), m.ReplacementTransform(date, tim.label),
                  run_time=1.2)

        # one triple: the rest goes behind a white veil
        until(self, v.at("statement"))
        veil = m.Rectangle(width=30, height=20, stroke_width=0, fill_color=m.WHITE, fill_opacity=0.8).set_z_index(5)
        triple = [obs, e_sensor, t99]
        for part in (*obs, *e_sensor, *t99):
            part.set_z_index(part.z_index + 10)
        spo = m.VGroup(txt("subject", 26, HEADING).next_to(obs.box, m.UP, buff=0.12),
                       txt("property", 26, HEADING).next_to(e_sensor.label, m.UP, buff=0.08),
                       txt("object", 26, HEADING).next_to(t99.box, m.DOWN, buff=0.12, aligned_edge=m.LEFT)).set_z_index(20)
        self.play(m.FadeIn(veil), run_time=0.5)
        self.play(m.LaggedStart(*[m.FadeIn(x, shift=0.1 * m.UP) for x in spo], lag_ratio=0.5), run_time=1.4)
        until(self, v.at("triple"))
        edges = [e_sensor, e_prop, e_foi, e_res, e_time]
        self.play(m.FadeOut(spo), m.FadeOut(veil), run_time=0.5)
        for part in (*obs, *e_sensor, *t99):
            part.set_z_index(part.z_index - 10)
        flashes = [m.ShowPassingFlash(e.tip_line.copy().set_stroke(HEADING, width=8, opacity=1), time_width=0.6)
                   for e in edges]
        self.play(m.LaggedStart(*flashes, lag_ratio=0.15), run_time=1.4)

        until(self, v.at("hosts"))
        e_host = edge(shw, t99, "hosts", avoid=nodes)
        half = m.Rectangle(width=0.22, height=shw.box.height, stroke_width=0,
                           fill_color=CAT["system"][1], fill_opacity=0.9)
        half.move_to(shw.box).align_to(shw.box, m.LEFT).set_z_index(1.5)
        tags = m.VGroup(txt("Platform", 20, CAT["system"][1]), txt("FeatureOfInterest", 20, "#8A8A00"))
        tags.arrange(m.RIGHT, buff=0.3).next_to(shw.box, m.DOWN, buff=0.12)
        self.play(grow(e_host))
        self.play(m.FadeIn(half), m.FadeIn(tags), run_time=0.8)

        # C: the Earth's atmosphere
        until(self, v.at("bigger"))
        mini = Globe(1.0, center=P["atm"] + 0.3 * m.DOWN).draw(10, 40, stroke=1.2)
        self.play(frame.animate.shift(PAN * m.RIGHT), run_time=1.4)
        self.play(m.FadeIn(mini, scale=0.8), run_time=0.8)
        until(self, v.at("atmosphere"))
        halo = m.Circle(radius=1.13, stroke_width=10, color=HEADING, stroke_opacity=0.35).move_to(mini[0])
        self.play(m.Create(halo), run_time=0.8)
        atm = ind("ex:EarthAtmosphere", "feature", icon=m.VGroup(mini, halo).copy().set(height=0.8)).move_to(P["atm"])
        e_atm = edge(air, atm, "isPropertyOf", avoid=nodes)
        self.play(m.FadeIn(atm.box), m.Create(atm.border),
                  m.ReplacementTransform(m.VGroup(mini, halo), atm.label[0]), m.FadeIn(atm.label[1]), run_time=1.4)
        self.play(grow(e_atm))

        # --- the classes: the same shape, without the identifiers
        graph = m.VGroup(obs, t99, shw, half, tags, air, val, tim, atm,
                         e_sensor, e_prop, e_foi, e_res, e_time, e_host, e_atm)
        until(self, v.at("shape"))
        self.play(frame.animate.move_to(graph.get_center()).set(width=graph.width + 1.6), run_time=1.5)
        C = {
            "obs": cls("Observation").move_to(obs.box), "t99": cls("Sensor").move_to(t99.box),
            "shw": cls_lines("Platform", "FeatureOfInterest").move_to(shw.box),
            "air": cls("Property").move_to(air.box), "atm": cls("FeatureOfInterest").move_to(atm.box),
            "val": cls("a value", context=True).move_to(val.box),
            "tim": cls("time:TemporalEntity", context=True).move_to(tim.box),
        }
        CE = [edge(C["obs"], C["t99"], "madeBySensor", dashed=False),
              edge(C["obs"], C["air"], "observedProperty", dashed=False, side=-1),
              edge(C["obs"], C["shw"], "hasFeatureOfInterest", dashed=False, side=-1),
              edge(C["obs"], C["val"], "hasResult", dashed=False, side=1),
              edge(C["obs"], C["tim"], "phenomenonTime", dashed=False, side=-1),
              edge(C["shw"], C["t99"], "hosts", dashed=False, side=1),
              edge(C["air"], C["atm"], "isPropertyOf", dashed=False, side=1)]
        inst = [obs, t99, shw, air, atm, val, tim]
        self.play(*[m.ReplacementTransform(a, b) for a, b in
                    zip(inst + [e_sensor, e_prop, e_foi, e_res, e_time, e_host, e_atm],
                        [C[k] for k in ("obs", "t99", "shw", "air", "atm", "val", "tim")] + CE)],
                  m.FadeOut(half), m.FadeOut(tags), run_time=2.0)
        until(self, v.at("classes"))
        model = m.VGroup(*C.values(), *CE)
        cap = txt("The classes and properties of SOSA", 30, HEADING).next_to(model, m.UP, buff=0.4)
        self.play(m.FadeIn(cap, shift=0.1 * m.DOWN), m.Circumscribe(C["obs"], color=HEADING), run_time=1.2)
        until(self, v.at("pattern"))
        self.play(m.Indicate(model, scale_factor=1.02, color=HEADING), run_time=1.2)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · historical-airtemp.ttl (abridged)", 20)
        self.play(m.FadeOut(m.VGroup(model, cap)), frame.animate.move_to(m.ORIGIN).set(width=m.config.frame_width),
                  run_time=1.0)
        ex.set(width=min(ex.width, 13.0)).move_to(0.15 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("lines"))
        for i in (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11):
            self.play(ex.line(i).animate.set_color(HEADING), run_time=0.22)

        # --- the end
        until(self, v.at("module"))
        end = end_card()
        self.play(m.FadeOut(ex), m.FadeOut(band), run_time=0.6)
        self.play(m.FadeIn(end), run_time=0.8)
        until(self, v.at("next"))
        nxt = txt("Stay tuned for more", 30, HEADING)
        nxt.to_edge(m.DOWN, buff=0.7)
        self.play(m.FadeIn(nxt, shift=0.1 * m.UP))
        until(self, v.end + 2.0)
