"""Episode 4 · SOSA Actuation: a window opens in Saint-Étienne, 18 April 2017 at 17:23.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/04-actuation/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/04-actuation/episode.yaml           MP4

Example from the spec: ssn/rdf/examples/open-window.ttl ("Simple Actuation to
open a window"), placed in Saint-Étienne (LocatedSampling.ttl). From the real
world to the model (video/scenarios.md): labelling (A) for the motor and the
value, the box that swallows the world (C) for the window. Then the classes,
side by side with those of episode 2: the same shape, other verbs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403
from globe import Globe  # noqa: E402

ST_ETIENNE = (4.387611, 45.437772)   # LocatedSampling.ttl
VIEW = (4.39, 39.0)                  # the centre of the globe when looking at Saint-Étienne
GLASS = "#E3EEF8"
HOLE = "#D9D9D9"

# The graph, in scene units (14.2 x 8 frame)
P = {
    "act": m.UP * 0.2,
    "prop": m.UP * 2.75,
    "win": m.RIGHT * 4.8 + m.UP * 2.3,
    "closer": m.RIGHT * 4.8 + m.DOWN * 1.2,
    "val": m.LEFT * 5.3 + m.UP * 0.2,
    "start": m.LEFT * 2.4 + m.DOWN * 2.7,
    "end": m.RIGHT * 2.4 + m.DOWN * 2.7,
}
# The classes: one layout for both modules, around the origin of the execution
Q = {"exe": (0, 0), "prop": (0, 2.5), "sys": (0, -2.5), "foi": (6.4, 0), "val": (-3.8, 0)}
ALONE = np.array([-1.6, 0, 0])       # the actuation's classes, alone
OBS, ACT = np.array([-8.1, 0, 0]), np.array([1.5, 0, 0])   # side by side, without the value
WIDE = 19.2                          # the frame width when they are side by side

LENS = np.array([3.8, 0.3, 0])

TURTLE = """\
ex:A188 a sosa:Actuation ;
  sosa:madeByActuator ex:closer-987 ;
  sosa:actsOnProperty ex:openState ;
  sosa:hasFeatureOfInterest ex:window98 ;
  sosa:hasSimpleResult true ;
  sosa:startTime "2017-04-18T17:23:00+02:00"^^xsd:dateTime ;
  sosa:endTime "2017-04-18T17:24:00+02:00"^^xsd:dateTime .

ex:window98 a sosa:FeatureOfInterest ;
  sosa:hasProperty ex:openState .
ex:openState a sosa:Property .
ex:closer-987 a ex:WindowCloser , sosa:Actuator ."""


# ------------------------------------------------------------- the real world, line-drawn
def building() -> m.VGroup:
    """The facade of the École des Mines, Saint-Étienne, simplified: the slate mansard roof and
    its dormers over the whole building; in front of it, the central block: the pediment with
    its bas-relief, the entablature with the inscription, four columns, two niches with their
    statues, the balcony carried by two statues on either side of the door, the steps. Name
    tablets under the windows. Returns (ground, facade, the window of the example)."""
    s = dict(stroke_width=2.2, color=INK)
    thin = dict(stroke_width=1.4, color=INK)
    stone = dict(fill_color="#FAFAFA", fill_opacity=1)
    base, cx, w = -2.6, -3.1, 3.3         # the ground, the axis and width of the central block
    f1, f2, top = base + 1.15, base + 2.25, base + 3.3   # the floors, the cornice
    x0, x1 = -6.8, 0.6                    # the facade

    def win(x: float, y: float, h: float = 0.6) -> m.Rectangle:
        return m.Rectangle(width=0.3, height=h, fill_color=GLASS, fill_opacity=1, **thin).move_to([x, y, 0])

    def tablet(x: float, y: float) -> m.Rectangle:
        return m.Rectangle(width=0.28, height=0.09, **thin).move_to([x, y, 0])

    def figure(x: float, y0: float, y1: float, arms: bool = False) -> m.VGroup:
        """A standing statue from y0 to y1: a robe, a head; `arms`: raised, carrying what is above."""
        h = y1 - y0
        robe = m.Polygon([x - 0.1, y0, 0], [x + 0.1, y0, 0], [x + 0.05, y0 + 0.78 * h, 0], [x - 0.05, y0 + 0.78 * h, 0],
                         fill_color="#F2F2F2", fill_opacity=1, **thin)
        head = m.Circle(radius=0.055, fill_color="#F2F2F2", fill_opacity=1, **thin).move_to([x, y0 + 0.86 * h, 0])
        out = m.VGroup(robe, head)
        if arms:
            out.add(*[m.Line([x + d * 0.05, y0 + 0.74 * h, 0], [x + d * 0.1, y1, 0], **thin) for d in (-1, 1)])
        return out

    def dormer(x: float) -> m.VGroup:
        """A dormer of the roof: a window under an arched top."""
        y0, y1 = top + 0.12, top + 0.5
        arc = [[x + 0.17 * np.cos(a), y1 + 0.08 * np.sin(a), 0] for a in np.linspace(0, np.pi, 9)]
        frame_ = m.Polygon([x - 0.17, y0, 0], [x + 0.17, y0, 0], *arc, [x - 0.17, y0, 0], **stone, **thin)
        return m.VGroup(frame_, m.Rectangle(width=0.2, height=0.3, fill_color=GLASS, fill_opacity=1, **thin)
                        .move_to([x, (y0 + y1) / 2, 0]))

    # the slate roof, over the whole facade, and the dormers of the wings
    roof = m.VGroup(m.Polygon([x0, top, 0], [x1, top, 0], [x1 - 0.2, top + 0.85, 0], [x0 + 0.2, top + 0.85, 0],
                              fill_color="#9DA3AB", fill_opacity=1, **s))
    walls = m.Rectangle(width=x1 - x0, height=top - base, **stone, **s).move_to([(x0 + x1) / 2, (base + top) / 2, 0])
    windows, tablets = m.VGroup(), m.VGroup()
    for a, b in ((x0, cx - w / 2), (cx + w / 2, x1)):
        for x in np.linspace(a + 0.42, b - 0.42, 3):
            roof.add(dormer(x))
            windows.add(win(x, base + 0.55, h=0.55), win(x, (f1 + f2) / 2 + 0.05, h=0.68), win(x, (f2 + top) / 2 + 0.05, h=0.55))
            tablets.add(tablet(x, f2 + 0.1))
    bands = m.VGroup(*[m.Line([x0 - 0.1, y, 0], [x1 + 0.1, y, 0], **thin) for y in (f1, f2)],
                     *[m.Line([x0, y, 0], [x1, y, 0], stroke_width=1, color=RULE)      # the rusticated ground floor
                       for y in np.linspace(base + 0.25, f1 - 0.2, 4)],
                     m.Line([x0 - 0.15, top, 0], [x1 + 0.15, top, 0], stroke_width=3, color=INK))

    # the central block, the entablature and its inscription, the pediment and its bas-relief
    block = m.Rectangle(width=w, height=top - base, **stone, **s).move_to([cx, (base + top) / 2, 0])
    entab = m.Rectangle(width=w + 0.2, height=0.3, **stone, **s).move_to([cx, top - 0.15, 0])
    sign = txt("ÉCOLE NATIONALE SUPÉRIEURE DES MINES", 11, INK).move_to(entab)
    pediment = m.Polygon([cx - w / 2 - 0.15, top, 0], [cx + w / 2 + 0.15, top, 0], [cx, top + 0.68, 0],
                         fill_color="#F2F2F2", fill_opacity=1, **s)
    inner = m.Polygon([cx - w / 2 + 0.2, top + 0.07, 0], [cx + w / 2 - 0.2, top + 0.07, 0], [cx, top + 0.55, 0], **thin)
    carve = dict(fill_color="#FAFAFA", fill_opacity=1, stroke_width=1.2, color=GREY)
    relief = m.VGroup(
        # the seated figure, at the centre, her drapery spread on either side
        m.Polygon([cx - 0.38, top + 0.08, 0], [cx + 0.38, top + 0.08, 0], [cx + 0.08, top + 0.34, 0],
                  [cx - 0.08, top + 0.34, 0], **carve),
        m.Polygon([cx - 0.07, top + 0.32, 0], [cx + 0.07, top + 0.32, 0], [cx + 0.05, top + 0.42, 0],
                  [cx - 0.05, top + 0.42, 0], **carve),
        m.Circle(radius=0.045, **carve).move_to([cx, top + 0.47, 0]),
        # the children, on either side
        *[m.VGroup(m.Ellipse(width=0.09, height=0.16, **carve).move_to([cx + d * 0.52, top + 0.17, 0]),
                   m.Circle(radius=0.04, **carve).move_to([cx + d * 0.52, top + 0.29, 0])) for d in (-1, 1)],
        # the reclining figures, at the ends
        *[m.VGroup(m.Ellipse(width=0.48, height=0.09, **carve).move_to([cx + d * 1.05, top + 0.12, 0]),
                   m.Circle(radius=0.04, **carve).move_to([cx + d * 0.8, top + 0.2, 0])) for d in (-1, 1)],
    )
    cols = m.VGroup()
    for dx in (-1.05, -0.35, 0.35, 1.05):
        y_lo, y_hi = f1 + 0.17, top - 0.3
        cols.add(m.Rectangle(width=0.14, height=y_hi - y_lo - 0.1, **stone, **thin).move_to([cx + dx, (y_lo + y_hi) / 2, 0]),
                 m.Rectangle(width=0.22, height=0.05, **stone, **thin).move_to([cx + dx, y_hi - 0.025, 0]),
                 m.Rectangle(width=0.22, height=0.05, **stone, **thin).move_to([cx + dx, y_lo + 0.025, 0]))
    for dx in (-0.7, 0, 0.7):
        windows.add(win(cx + dx, (f1 + f2) / 2 + 0.1, h=0.62), win(cx + dx, (f2 + top) / 2 - 0.12, h=0.5))
        tablets.add(tablet(cx + dx, f2 + 0.02))
    niches = m.VGroup()
    for dx in (-1.42, 1.42):
        arch = m.VMobject(**thin).set_points_as_corners(
            [[cx + dx - 0.12, f1 + 0.22, 0], [cx + dx - 0.12, f1 + 0.7, 0],
             *[[cx + dx + 0.12 * np.cos(a), f1 + 0.7 + 0.12 * np.sin(a), 0] for a in np.linspace(np.pi, 0, 9)],
             [cx + dx + 0.12, f1 + 0.22, 0], [cx + dx - 0.12, f1 + 0.22, 0]])
        niches.add(arch, figure(cx + dx, f1 + 0.24, f1 + 0.76), m.Circle(radius=0.08, **thin).move_to([cx + dx, f2 + 0.55, 0]))

    # the ground floor: the balcony, carried by two statues on either side of the door
    balcony = m.VGroup(m.Line([cx - 1.2, f1 + 0.02, 0], [cx + 1.2, f1 + 0.02, 0], stroke_width=3, color=INK),
                       *[m.Line([x, f1 + 0.02, 0], [x, f1 + 0.17, 0], **thin) for x in np.linspace(cx - 1.1, cx + 1.1, 15)],
                       m.Line([cx - 1.2, f1 + 0.17, 0], [cx + 1.2, f1 + 0.17, 0], **thin))
    carry = m.VGroup(*[m.VGroup(m.Rectangle(width=0.24, height=0.14, **stone, **thin).move_to([cx + dx, base + 0.19, 0]),
                                figure(cx + dx, base + 0.26, f1, arms=True)) for dx in (-0.42, 0.42)])
    door = m.VGroup(m.Rectangle(width=0.4, height=0.75, fill_color=GLASS, fill_opacity=1, **thin).move_to([cx, base + 0.5, 0]),
                    m.Line([cx, base + 0.12, 0], [cx, base + 0.75, 0], **thin))
    for dx in (-1.05, 1.05):
        windows.add(win(cx + dx, base + 0.55, h=0.55))
    steps = m.VGroup(*[m.Line([cx - 0.35 - 0.12 * k, base + 0.12 - 0.04 * k, 0], [cx + 0.35 + 0.12 * k, base + 0.12 - 0.04 * k, 0],
                              **thin) for k in range(3)])
    target = windows[13]                 # the right wing, first floor, middle window: the director's office
    ground = m.Line([x0 - 0.2, base, 0], [x1 + 0.3, base, 0], stroke_width=2, color=GREY)
    facade = m.VGroup(roof, walls, bands, block, cols, entab, sign, pediment, inner, relief, niches, tablets,
                      balcony, carry, door, steps, windows)
    return m.VGroup(ground, facade, target)


def window(op: m.ValueTracker, spin: m.ValueTracker, c) -> tuple[m.VGroup, m.VGroup]:
    """The window seen up close: a top-hung sash, pushed open by a chain motor on
    the sill. `op` from 0 (closed) to 1 (open); `spin` turns the motor's wheel.
    Returns (the window, the motor)."""
    c = np.asarray(c, float)
    W, H = 2.0, 2.4
    s = dict(stroke_width=2.5, color=INK)
    top, bottom = c[1] + H / 2, c[1] - H / 2
    x0, x1 = c[0] - W / 2, c[0] + W / 2
    frame = m.Rectangle(width=W + 0.3, height=H + 0.7, fill_color="#FAFAFA", fill_opacity=1, **s)
    frame.move_to([c[0], c[1] - 0.2, 0])
    hole = m.Rectangle(width=W, height=H, fill_color=HOLE, fill_opacity=1, stroke_width=1.6, color=INK).move_to(c)

    def yb() -> float:
        return bottom + 0.3 * H * op.get_value()

    def sash() -> m.VGroup:
        dx = 0.22 * op.get_value()      # the bottom comes towards us
        y = yb()
        out = m.Polygon([x0, top, 0], [x1, top, 0], [x1 + dx, y, 0], [x0 - dx, y, 0],
                        fill_color=GLASS, fill_opacity=1, **s)
        glint = m.Line([x0 + 0.3, y + 0.25 * (top - y), 0], [x0 + 0.75, y + 0.65 * (top - y), 0],
                       stroke_width=2, color=m.WHITE)
        return m.VGroup(out, glint)

    pane = m.always_redraw(sash)
    arm = m.always_redraw(lambda: m.Line([c[0], bottom, 0], [c[0], max(yb(), bottom + 0.01), 0],
                                         stroke_width=5, color=GREY))
    box = m.Rectangle(width=0.9, height=0.34, fill_color="#E6E6E6", fill_opacity=1, **s)
    box.move_to([c[0], bottom - 0.27, 0])
    hub = m.Circle(radius=0.11, stroke_width=1.6, color=INK).move_to(box)
    spoke = m.always_redraw(lambda: m.Line(
        hub.get_center(), hub.get_center() + 0.11 * np.array([np.cos(spin.get_value()), np.sin(spin.get_value()), 0]),
        stroke_width=1.6, color=INK))
    return m.VGroup(frame, hole, pane, arm), m.VGroup(box, hub, spoke)


def shape(names: dict[str, str], verbs: tuple[str, str], origin) -> tuple[dict, dict]:
    """The class shape shared by observations and actuations, around `origin`:
    `names` gives the class of each node of Q (the value, `val`, is optional),
    `verbs` the two properties that differ (made by…, …property)."""
    C = {k: cls(n, 24, context=(k == "val")).move_to(origin + [*Q[k], 0]) for k, n in names.items()}
    E = {"made": edge(C["exe"], C["sys"], verbs[0], dashed=False, size=22, side=1),
         "prop": edge(C["exe"], C["prop"], verbs[1], dashed=False, size=22, side=-1),
         "foi": edge(C["exe"], C["foi"], "hasFeatureOfInterest", dashed=False, size=22, side=1, label_pos=0.45)}
    if "val" in C:
        E["res"] = edge(C["exe"], C["val"], "hasResult", dashed=False, size=22, side=1)
        E["has"] = edge(C["foi"], C["prop"], "hasProperty", dashed=False, size=22, side=-1,
                        avoid=[E["foi"].label, E["prop"].label])
    return C, E


# ------------------------------------------------------------- the scene
class Episode04(m.Scene):
    def construct(self) -> None:
        v = Voice()
        frame = self.camera.frame

        # --- the title card
        card = title_card("Episode 4 · Actuations", "The SOSA Actuation module")
        self.add(card)
        until(self, v.at("globe") - 0.7)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- the planet: sensors, then actuators
        g = Globe(3.4)
        lon, lat = m.ValueTracker(-30), m.ValueTracker(15)
        dots, rings = m.ValueTracker(0), m.ValueTracker(0)
        rng = np.random.default_rng(7)
        z = rng.uniform(-1, 1, 500)
        sens = np.column_stack([rng.uniform(-180, 180, 500), np.degrees(np.arcsin(z))])
        z = rng.uniform(-1, 1, 160)
        acts = np.column_stack([rng.uniform(-180, 180, 160), np.degrees(np.arcsin(z))])

        def earth():
            l0, p0 = lon.get_value(), lat.get_value()
            out = g.draw(l0, p0)
            if dots.get_value() > 0.01:
                out.add(g.sensors(l0, p0, sens, opacity=dots.get_value()))
            if rings.get_value() > 0.01:
                xy, cosc = __import__("globe").ortho(np.radians(acts), l0, p0)
                out.add(m.VGroup(*[m.Circle(radius=0.07, stroke_width=2.5, color=CAT["system"][1],
                                            stroke_opacity=rings.get_value()).move_to(p)
                                   for p in g.to_scene(xy[cosc > 0.05])]))
            return out

        world = m.always_redraw(earth)
        self.play(m.FadeIn(world), dots.animate.set_value(1), lon.animate.set_value(-18), run_time=2.0,
                  rate_func=m.linear)
        until(self, v.at("actuators"))
        self.play(rings.animate.set_value(1), dots.animate.set_value(0.35), lon.animate.set_value(-5),
                  run_time=2.2, rate_func=m.linear)
        until(self, v.at("france"))
        self.play(lon.animate.set_value(VIEW[0]), lat.animate.set_value(VIEW[1]), dots.animate.set_value(0),
                  rings.animate.set_value(0), run_time=2.4)
        world.clear_updaters()
        self.remove(world)
        fine = Globe(3.4, detail="50m", borders=True).draw(*VIEW)
        here = g.point(*VIEW, *ST_ETIENNE)
        self.add(fine)
        pin_dot = m.Dot(here, radius=0.07, color=HEADING)
        self.play(m.FadeIn(pin_dot, scale=3), m.Flash(here, color=HEADING, line_length=0.15), run_time=0.8)

        until(self, v.at("april"))
        name = txt("Saint-Étienne", 30, HEADING).next_to(here, m.UR, buff=0.15)
        name = m.VGroup(m.BackgroundRectangle(name, color=m.WHITE, fill_opacity=0.85, buff=0.08), name)
        self.play(fine.animate.scale(14, about_point=here), m.FadeIn(name), run_time=2.5)
        self.play(m.FadeOut(m.VGroup(fine, pin_dot, name)), run_time=0.6)

        # --- the building, the window, the motor
        ground, facade, target = building()
        place = txt("École des Mines, Saint-Étienne", 22, GREY).move_to([-3.1, -3.05, 0])
        until(self, v.at("building"))
        self.play(m.Create(ground), m.Create(facade, lag_ratio=0.1), m.FadeIn(place), run_time=1.8)
        op, spin = m.ValueTracker(0), m.ValueTracker(0)
        lens = m.Circle(radius=2.6, stroke_width=2, color=GREY, fill_color=m.WHITE, fill_opacity=1).move_to(LENS)
        rays = m.VGroup(m.Line(target.get_corner(m.UR), lens.point_at_angle(np.radians(160)), stroke_width=1.5, color=GREY),
                        m.Line(target.get_corner(m.DR), lens.point_at_angle(np.radians(205)), stroke_width=1.5, color=GREY))
        win, motor = window(op, spin, LENS + 0.25 * m.UP)
        # once a graph box (z-index 1 to 3) is on stage, ordering follows the z-index: so we set it
        # for the magnifier and its contents too
        lens.set_z_index(0.1)
        win.set_z_index(0.2)
        motor.set_z_index(0.3)
        self.play(m.Indicate(target, scale_factor=1.3, color=HEADING), run_time=0.8)
        self.play(m.Create(rays), m.GrowFromPoint(lens, target.get_center()), run_time=0.9)
        self.play(m.FadeIn(win), run_time=0.6)
        until(self, v.at("motor"))
        self.play(m.FadeIn(motor, scale=1.2), m.Circumscribe(motor[0], color=GREY, buff=0.08), run_time=1.0)

        until(self, v.at("date"))
        clock = txt("18 April 2017 · 17:23", 28, GREY).move_to(LENS + 3.05 * m.DOWN).set_z_index(0.5)
        self.play(m.FadeIn(clock, shift=0.1 * m.DOWN))
        until(self, v.at("turn"))
        self.play(spin.animate.set_value(6 * np.pi), op.animate.set_value(0.25), run_time=1.6, rate_func=m.linear)
        until(self, v.at("open"))
        later = txt("18 April 2017 · 17:24", 28, GREY).move_to(clock).set_z_index(0.5)
        self.play(spin.animate.set_value(16 * np.pi), op.animate.set_value(1), m.Transform(clock, later),
                  run_time=1.6)

        # --- from the real world to the model
        band = hud("SOSA · Actuation module")
        until(self, v.at("identifier"))
        iri = mono("https://example.org/data/window98", 22).next_to(lens, m.UP, buff=0.15).set_z_index(0.5)
        iri.shift(0.6 * m.LEFT)
        self.play(m.FadeIn(band), m.Write(iri), run_time=1.0)
        pin(self, band)

        # C: the window shrinks into its yellow box; the motor stays where it is
        until(self, v.at("window"))
        win[2].clear_updaters()
        win[3].clear_updaters()
        thumb = m.VGroup(win[0], win[1], win[2]).copy().set(height=0.9)
        wnode = ind("ex:window98", "feature", sub="director's office", icon=thumb).move_to(P["win"])
        self.play(m.FadeOut(m.VGroup(rays, place, ground, facade, target, lens)), m.FadeOut(win[3]),
                  m.FadeIn(wnode.box), m.Create(wnode.border),
                  m.ReplacementTransform(m.VGroup(win[0], win[1], win[2]), wnode.label[0]),
                  m.TransformMatchingShapes(iri, wnode.label[1]), run_time=1.6)
        until(self, v.at("state"))
        prop = ind("ex:openState", "property").move_to(P["prop"])
        nodes = [wnode, prop, clock, motor]
        e_has = edge(wnode, prop, "hasProperty", side=1, avoid=nodes)
        self.play(appear(prop, 0.8))
        self.play(grow(e_has))

        # A: the motor gets an orange dashed outline, then becomes its node
        until(self, v.at("actuator"))
        closer = ind("ex:closer-987", "system", sub="window motor").move_to(P["closer"])
        spoke = motor[2]
        spoke.clear_updaters()
        ring = m.DashedVMobject(m.Rectangle(width=1.4, height=0.8, color=CAT["system"][1], stroke_width=3),
                                num_dashes=40, dashed_ratio=0.45).move_to(motor).set_z_index(0.5)
        self.play(m.Create(ring), run_time=0.6)
        self.play(m.FadeIn(closer.box), m.ReplacementTransform(ring, closer.border),
                  m.ReplacementTransform(motor, closer.label), run_time=1.2)

        # --- the graph builds up
        until(self, v.at("actuation"))
        act = ind("ex:A188", "execution", sub="an actuation").move_to(P["act"])
        val = value("true").move_to(P["val"])
        start = value("2017-04-18T17:23+02:00", 22).move_to(P["start"])
        end = value("2017-04-18T17:24+02:00", 22).move_to(P["end"])
        nodes = [act, wnode, prop, closer, val, start, end, e_has.label]
        self.play(appear(act, 1.0))

        until(self, v.at("made"))
        e_made = edge(act, closer, "madeByActuator", side=-1, avoid=nodes)
        nodes.append(e_made.label)
        self.play(grow(e_made))
        until(self, v.at("acts"))
        e_acts = edge(act, prop, "actsOnProperty", side=1, avoid=nodes)
        nodes.append(e_acts.label)
        self.play(grow(e_acts))
        until(self, v.at("interest"))
        e_foi = edge(act, wnode, "hasFeatureOfInterest", side=1, avoid=nodes)
        nodes.append(e_foi.label)
        self.play(grow(e_foi), m.Indicate(wnode, scale_factor=1.05, color=CAT["feature"][1]))

        until(self, v.at("result"))
        e_res = edge(act, val, "hasSimpleResult", side=1, avoid=nodes)
        nodes.append(e_res.label)
        self.play(grow(e_res))
        self.play(appear(val, 0.6))
        until(self, v.at("true"))
        self.play(m.Indicate(val, scale_factor=1.15, color=HEADING), m.Indicate(prop, scale_factor=1.05), run_time=0.9)
        until(self, v.at("started"))
        e_start = edge(act, start, "startTime", side=1, avoid=nodes)
        nodes.append(e_start.label)
        self.play(grow(e_start), m.FadeIn(start.box), m.Create(start.border),
                  m.ReplacementTransform(clock, start.label), run_time=1.2)
        until(self, v.at("ended"))
        e_end = edge(act, end, "endTime", side=-1, avoid=nodes)
        self.play(grow(e_end), appear(end, 0.8), run_time=1.2)

        # --- the classes: the shape without the identifiers, then side by side with the observation
        until(self, v.at("shape"))
        A, AE = shape({"exe": "Actuation", "prop": "Property", "foi": "FeatureOfInterest", "sys": "Actuator",
                       "val": "a value"}, ("madeByActuator", "actsOnProperty"), ALONE)
        inst = [act, prop, wnode, closer, val, e_made, e_acts, e_foi, e_res, e_has]
        target_ = [A["exe"], A["prop"], A["foi"], A["sys"], A["val"], AE["made"], AE["prop"], AE["foi"], AE["res"],
                   AE["has"]]
        self.play(*[m.ReplacementTransform(a, b) for a, b in zip(inst, target_)],
                  m.FadeOut(m.VGroup(start, end, e_start, e_end)),
                  run_time=2.0)
        act_shape = m.VGroup(*A.values(), *AE.values())
        until(self, v.at("familiar"))
        self.play(m.Indicate(act_shape, scale_factor=1.03, color=HEADING), run_time=1.0)

        until(self, v.at("vienna"))
        O, OE = shape({"exe": "Observation", "prop": "Property", "foi": "FeatureOfInterest", "sys": "Sensor"},
                      ("madeBySensor", "observedProperty"), OBS)
        obs_shape = m.VGroup(*O.values(), *OE.values())
        # side by side, the value and hasProperty would not fit: they go
        aside = m.VGroup(A.pop("val"), AE.pop("res"), AE.pop("has"))
        act_shape = m.VGroup(*A.values(), *AE.values())
        mid = Q["foi"][0] / 2
        heads = m.VGroup(txt("Observation · episode 2", 30, HEADING).move_to(OBS + [mid, 3.6, 0]),
                         txt("Actuation · this episode", 30, HEADING).move_to(ACT + [mid, 3.6, 0]))
        self.play(m.FadeOut(aside), act_shape.animate.shift(ACT - ALONE),
                  frame.animate.set(width=WIDE).move_to(m.ORIGIN), run_time=1.2)
        self.play(m.FadeIn(obs_shape, shift=0.2 * m.RIGHT), m.FadeIn(heads), run_time=1.0)

        def verb(e: Edge, node: Node) -> m.Animation:
            return m.AnimationGroup(e.label.animate.set_color(HEADING), e.tip_line.animate.set_color(HEADING),
                                    m.Circumscribe(node, color=HEADING, buff=0.08), run_time=0.9)

        until(self, v.at("sensor"))
        self.play(verb(OE["made"], O["sys"]))
        until(self, v.at("observes"))
        self.play(verb(OE["prop"], O["prop"]))
        until(self, v.at("byactuator"))
        self.play(verb(AE["made"], A["sys"]))
        until(self, v.at("actson"))
        self.play(verb(AE["prop"], A["prop"]))

        until(self, v.at("know"))
        self.play(m.Indicate(obs_shape, scale_factor=1.03, color=HEADING), run_time=1.0)
        until(self, v.at("itself"))
        self.play(m.Indicate(act_shape, scale_factor=1.03, color=HEADING), run_time=1.0)

        # --- the procedure
        until(self, v.at("procedure"))
        here_ = np.array([-1.5, 0, 0])
        self.play(m.FadeOut(obs_shape), m.FadeOut(heads), act_shape.animate.shift(here_ - ACT), run_time=1.2)
        proc = cls("ActuatingProcedure", 24).move_to(here_ + [-3.7, -2.5, 0])
        e_proc = edge(A["exe"], proc, "usedProcedure", dashed=False, size=22, side=1,
                      avoid=[A["sys"], AE["made"].label])
        self.play(m.FadeIn(proc.box), m.Create(proc.border), m.Write(proc.label), grow(e_proc), run_time=1.2)
        until(self, v.at("rule"))
        rule = note_box("A rule", ["If the room gets too warm,", "open the window."], 24)
        rule.move_to(proc.get_center() + [-0.8, 3.5, 0])
        self.play(m.FadeIn(rule, shift=0.1 * m.RIGHT), m.Circumscribe(proc, color=HEADING), run_time=1.0)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · open-window.ttl (abridged)", 20)
        self.play(m.FadeOut(m.VGroup(act_shape, proc, e_proc, rule)),
                  frame.animate.move_to(m.ORIGIN).set(width=m.config.frame_width), run_time=1.0)
        ex.set(width=min(ex.width, 13.0)).move_to(0.15 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        until(self, v.at("lines"))
        for i in (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11):
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
