"""Episode 8 · Sample Relations: what one arrow between two samples does not say.

The voice leads: each step waits for its mark (`v.at(id)`, the `mark`s of
episode.yaml). Through video/narrated.sh, never directly: the scene reads
timeline.json via NARRATION_TIMELINE.

    video/narrated.sh video/episodes/08-sample-relations/episode.yaml --dry     storyboard
    video/narrated.sh video/episodes/08-sample-relations/episode.yaml           MP4

The isSampleOf arrow of episode 3, which does not say how; the qualified
relation of the Sample Relations module (sample-relations.ttl, namespace
sosa-rel:); the spec's example (rdf/examples/sample-relations.ttl): a rock
specimen, its polished mount 7, and spot 1 under a microprobe. Real world →
model: the box that swallows the world (C), since all three are samples.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # video/
from charter import *  # noqa: E402,F403

ROCK = "#CFC6B5"
GRAIN = "#A89F8E"
RESIN = "#F4E9C8"
CORE = "#DCEBF5"

# the instance graph: the specimen and its mount on the left; spot 1, its relationship
# and the nature of that relationship in a column on the right
P = {
    "specimen": [-4.6, 2.3, 0], "mount": [-4.6, -0.2, 0],
    "spot": [3.4, 2.3, 0], "rel": [3.4, -0.2, 0], "nature": [3.4, -2.55, 0],
}

# the natures of RelationshipNature (its skos:example in sample-relations.ttl)
NATURES = ["Split of core sample", "Specimen taken from borehole", "Adjacent flight-line",
           "Probe spot on polished specimen"]

TURTLE = """\
relex:CSRWA25569-mount7
  rdf:type sosa:Sample ;
  rdfs:label "CSRWA25569 mount 7" ;
  sosa:isSampleOf relex:CSRWA25569 ;
.
relex:CSRWA25569-mount7-spot1
  rdf:type sosa:Sample ;
  rdfs:label "spot 1" ;
  sosa-rel:hasSampleRelationship [
      rdf:type sosa-rel:SampleRelationship ;
      sosa-rel:natureOfRelationship [
          rdf:type sosa-rel:RelationshipNature ;
          rdfs:comment "probe spot on polished mount" ;
        ] ;
      sosa-rel:relatedSample relex:CSRWA25569-mount7 ;
    ] ;
."""


# ------------------------------------------------------------- the real world, line-drawn
def rock(r: float = 1.0) -> m.VGroup:
    """A rock specimen: an irregular outline, a few grains."""
    ks = [1.0, 0.82, 0.95, 1.08, 0.9, 0.78, 1.0, 0.92, 1.05]
    pts = [[r * k * np.cos(a), 0.72 * r * k * np.sin(a), 0] for a, k in
           zip(np.linspace(0, 2 * np.pi, len(ks), endpoint=False) + 0.2, ks)]
    body = m.Polygon(*pts, fill_color=ROCK, fill_opacity=1, stroke_width=3, color=INK)
    grains = m.VGroup(*[m.Polygon(*[[x + 0.14 * r * np.cos(a), y + 0.1 * r * np.sin(a), 0]
                                    for a in np.linspace(0, 2 * np.pi, 5, endpoint=False) + x],
                                  fill_color=GRAIN, fill_opacity=1, stroke_width=0)
                        for x, y in ((-0.45 * r, 0.15 * r), (0.2 * r, -0.25 * r), (0.5 * r, 0.25 * r))])
    return m.VGroup(body, grains)


def mount(r: float = 1.25) -> m.VGroup:
    """A polished mount: a disc of resin, a slice of the rock set in it."""
    disc = m.Circle(radius=r, fill_color=RESIN, fill_opacity=1, stroke_width=3, color=INK)
    rim = m.Circle(radius=r * 0.9, stroke_width=1.5, color="#C9B98A")
    return m.VGroup(disc, rim)


def probe() -> m.VGroup:
    """The microprobe column, above the mount."""
    s = dict(stroke_width=3, color=INK, fill_color="#E6E6E6", fill_opacity=1)
    body = m.Rectangle(width=1.1, height=0.9, **s)
    cone = m.Polygon([-0.55, 0, 0], [0.55, 0, 0], [0.12, -0.6, 0], [-0.12, -0.6, 0], **s)
    cone.next_to(body, m.DOWN, buff=0)
    return m.VGroup(body, cone)


def core_icon() -> m.VGroup:
    body = m.RoundedRectangle(width=0.22, height=0.9, corner_radius=0.06, stroke_width=2, color=INK,
                              fill_color=CORE, fill_opacity=1)
    return m.VGroup(body)


def bubble_icon() -> m.VGroup:
    b = m.Circle(radius=0.22, stroke_width=2, color=INK, fill_color=m.WHITE, fill_opacity=1)
    shine = m.Arc(radius=0.13, start_angle=1.9, angle=1.0, stroke_width=2, color=LIGHTGREY).move_to(b).shift(
        [-0.06, 0.06, 0])
    return m.VGroup(b, shine)


def pair(a: Node, b: Node, dy: float) -> tuple[Node, Node]:
    """Copies of two boxes moved by `dy`: two arrows between the same classes, one above the other."""
    return (Node(a.box.copy().shift(dy * m.UP), a.border, a.label),
            Node(b.box.copy().shift(dy * m.UP), b.border, b.label))


class Episode08(m.Scene):
    def link(self, a, b, name, nodes, **kw) -> Edge:
        """An arrow whose label avoids the nodes and the labels already placed;
        its own is added to the list."""
        e = edge(a, b, name, avoid=nodes, size=21, **kw)
        if e.label is not None:
            nodes.append(e.label)
        return e

    def construct(self) -> None:
        v = Voice()

        # --- the title card
        card = title_card("Episode 8 · Sample relations", "The Sample Relations extension module")
        self.add(card)
        until(self, v.at("bubble") - 0.4)
        self.play(m.FadeOut(card), run_time=0.6)

        # --- episode 3: one arrow
        band = hud("Sample Relations module")
        bub = ind("ex:Bubble873", "feature", sub="a bubble of air", icon=bubble_icon()).move_to([-3.6, 1.3, 0])
        core = ind("ex:IceCore12", "feature", sub="ice core", icon=core_icon()).move_to([3.6, 1.3, 0])
        where = txt("Episode 3 · Antarctica", 24, GREY).move_to([0, 3.1, 0])
        self.play(m.FadeIn(band), appear(bub), appear(core), m.FadeIn(where), run_time=1.0)
        pin(self, band)
        until(self, v.at("arrow"))
        is_of = edge(bub, core, "sosa:isSampleOf", dashed=True)
        self.play(grow(is_of, 1.0))

        # one arrow does not say how
        until(self, v.at("how"))
        q = txt("?", 72, HEADING, weight=m.BOLD).next_to(is_of.line, m.DOWN, buff=0.35)
        self.play(m.FadeIn(q, scale=0.6), m.FadeOut(where), run_time=0.6)
        tags = {k: tag(s, 24, GREY) for k, s in (("split", "split of a core sample"), ("crushed", "crushed"),
                                                 ("station", "station along a traverse"),
                                                 ("pixel", "pixel within an image"))}
        tags["split"].move_to([-3.4, -1.3, 0])
        tags["crushed"].move_to([3.4, -1.3, 0])
        tags["station"].move_to([-3.0, -2.5, 0])
        tags["pixel"].move_to([3.0, -2.5, 0])
        until(self, v.at("split"))
        self.play(m.FadeIn(tags["split"], shift=0.1 * m.UP), run_time=0.5)
        self.play(m.FadeIn(tags["crushed"], shift=0.1 * m.UP), run_time=0.5)
        until(self, v.at("station"))
        self.play(m.FadeIn(tags["station"], shift=0.1 * m.UP), run_time=0.5)
        until(self, v.at("pixel"))
        self.play(m.FadeIn(tags["pixel"], shift=0.1 * m.UP), run_time=0.5)

        # --- the arrow becomes a node
        until(self, v.at("module"))
        ns = m.VGroup(mono("sosa-rel:", 26, HEADING), txt("Sample Relations", 26, GREY)).arrange(m.RIGHT, buff=0.25)
        ns.move_to([0, 2.95, 0])
        self.play(m.FadeIn(ns, shift=0.1 * m.DOWN), run_time=0.7)
        until(self, v.at("node"))
        rel = ind("[ ]", "individual", 24, sub="a SampleRelationship").move_to([0, -0.9, 0])
        nodes = [bub, core, rel, ns]
        e_has = self.link(bub, rel, "hasSampleRelationship", nodes)
        e_rel = self.link(rel, core, "relatedSample", nodes)
        self.play(m.FadeOut(q), m.FadeOut(m.VGroup(*tags.values())), run_time=0.4)
        self.play(m.ReplacementTransform(is_of, m.VGroup(e_has, e_rel)), appear(rel), run_time=1.2)
        until(self, v.at("kind"))
        nat = ind("[ ]", "individual", 24, sub="its nature").move_to([0, -2.85, 0])
        e_nat = self.link(rel, nat, "natureOfRelationship", nodes + [nat])
        self.play(grow(e_nat, 0.7), appear(nat, 0.7), run_time=1.0)
        self.play(m.Indicate(nat, color=HEADING, scale_factor=1.06), run_time=0.8)

        # --- the spec's example: a specimen, a mount, a spot
        until(self, v.at("geology"))
        self.play(m.FadeOut(m.VGroup(bub, core, rel, nat, e_has, e_rel, e_nat, ns)), run_time=0.6)
        stone = rock(1.4).move_to([-4.0, 0.6, 0])
        stone_l = txt("Specimen CSRWA25569", 24, GREY).next_to(stone, m.DOWN, buff=0.35)
        self.play(m.DrawBorderThenFill(stone[0]), m.FadeIn(stone[1]), m.FadeIn(stone_l), run_time=1.2)

        until(self, v.at("cut"))
        saw = m.DashedLine([-3.4, 1.9, 0], [-3.4, -0.3, 0], dash_length=0.12, stroke_width=3, color=HEADING)
        self.play(m.Create(saw), run_time=0.6)
        slab = rock(0.7).move_to([-3.4, 0.6, 0])
        disc = mount().move_to([0.6, 0.3, 0])
        self.add(slab)
        self.play(m.FadeOut(saw), slab.animate.move_to(disc), run_time=0.9)
        self.play(m.DrawBorderThenFill(disc[0]), m.Create(disc[1]), run_time=0.8)
        self.bring_to_front(slab)
        shine = m.Line([-0.6, 1.2, 0], [1.8, -0.6, 0], stroke_width=10, color=m.WHITE)
        self.play(m.ShowPassingFlash(shine, time_width=0.5), run_time=0.7)

        until(self, v.at("mount"))
        disk = m.VGroup(disc, slab)
        disk_l = txt("CSRWA25569 mount 7", 24, GREY).next_to(disk, m.DOWN, buff=0.35)
        self.play(m.FadeIn(disk_l), m.Indicate(disk, color=HEADING, scale_factor=1.04), run_time=0.8)

        until(self, v.at("probe"))
        spot_xy = slab.get_center() + np.array([0.18, 0.12, 0])
        col = probe().move_to([spot_xy[0], 3.0, 0])
        self.play(m.FadeIn(col, shift=0.4 * m.DOWN), run_time=0.8)
        beam = m.Line(col.get_bottom(), spot_xy, stroke_width=4, color=HEADING)
        self.play(m.Create(beam), run_time=0.5)
        until(self, v.at("spot"))
        dot = m.Dot(spot_xy, radius=0.06, color=INK)
        cross = m.Circle(radius=0.2, stroke_width=2, color=INK).move_to(spot_xy)
        spot = m.VGroup(dot, cross)
        spot_l = txt("spot 1", 24, GREY).next_to(disk, m.RIGHT, buff=0.6).shift(0.3 * m.UP)
        pointer = m.Line(spot_l.get_left() + 0.1 * m.LEFT, spot_xy + 0.2 * m.RIGHT, stroke_width=1.5, color=GREY)
        self.play(m.FadeIn(spot, scale=2.5), m.FadeOut(beam), run_time=0.6)
        self.play(m.FadeIn(spot_l), m.Create(pointer), run_time=0.6)

        # --- the three samples shrink into their yellow boxes (C)
        until(self, v.at("too"))
        sp_n = ind("relex:CSRWA25569", "feature", 20, sub="Specimen CSRWA25569",
                   icon=stone.copy().set(height=0.45)).move_to(P["specimen"])
        mt_n = ind("relex:CSRWA25569-mount7", "feature", 20, sub="CSRWA25569 mount 7",
                   icon=disk.copy().set(height=0.45)).move_to(P["mount"])
        st_n = ind("relex:CSRWA25569-mount7-spot1", "feature", 20, sub="spot 1",
                   icon=m.VGroup(disk, spot).copy().set(height=0.45)).move_to(P["spot"])
        self.play(m.FadeOut(m.VGroup(col, pointer, stone_l, disk_l, spot_l)), run_time=0.4)
        self.play(m.FadeIn(sp_n.box), m.Create(sp_n.border), m.ReplacementTransform(stone, sp_n.label[0]),
                  m.FadeIn(sp_n.label[1]),
                  m.FadeIn(mt_n.box), m.Create(mt_n.border), m.TransformFromCopy(disk, mt_n.label[0]),
                  m.FadeIn(mt_n.label[1]),
                  m.FadeIn(st_n.box), m.Create(st_n.border), m.ReplacementTransform(m.VGroup(disk, spot),
                                                                                    st_n.label[0]),
                  m.FadeIn(st_n.label[1]), run_time=1.6)
        nodes = [sp_n, mt_n, st_n]
        e_of = self.link(mt_n, sp_n, "isSampleOf", nodes, side=-1)
        self.play(grow(e_of, 0.8))

        until(self, v.at("points"))
        rel = ind("[ ]", "individual", 22, sub="a SampleRelationship").move_to(P["rel"])
        nodes.append(rel)
        e_has = self.link(st_n, rel, "hasSampleRelationship", nodes)
        e_to = self.link(rel, mt_n, "relatedSample", nodes)
        self.play(grow(e_has, 0.8), appear(rel, 0.8), run_time=1.2)
        self.play(grow(e_to, 0.8))
        until(self, v.at("nature"))
        nat = ind("[ ]", "individual", 22, sub="probe spot on polished mount").move_to(P["nature"])
        nodes.append(nat)
        e_nat = self.link(rel, nat, "natureOfRelationship", nodes, side=-1)
        self.play(grow(e_nat, 0.8), appear(nat, 0.8), run_time=1.2)
        graph = m.VGroup(sp_n, mt_n, st_n, rel, nat, e_of, e_has, e_to, e_nat)

        # --- the classes of the module
        until(self, v.at("classes"))
        sample = cls("sosa:Sample", 28).move_to([-4.9, 1.8, 0])
        sr = cls("SampleRelationship", 28).move_to([2.9, 1.8, 0])
        rn = cls("RelationshipNature", 28).move_to([2.9, -0.6, 0])
        concept = cls("skos:Concept", 28, context=True).move_to([2.9, -2.5, 0])
        a_up, b_up = pair(sample, sr, 0.24)
        b_dn, a_dn = pair(sr, sample, -0.24)
        c_has = edge(a_up, b_up, "hasSampleRelationship", dashed=False, size=22)
        c_rel = edge(b_dn, a_dn, "relatedSample", dashed=False, size=22, side=1)
        c_nat = edge(sr, rn, "natureOfRelationship", dashed=False, size=22, side=-1)
        c_sub = edge(rn, concept, None, dashed=False, open_tip=True)
        self.play(m.FadeOut(graph), run_time=0.6)
        self.play(appear(sample), appear(sr), grow(c_has), run_time=1.0)
        self.play(grow(c_rel), run_time=0.7)
        self.play(grow(c_nat), appear(rn), run_time=0.9)
        until(self, v.at("concept"))
        self.play(grow(c_sub, 0.6), appear(concept, 0.6), run_time=0.9)

        until(self, v.at("few"))
        ex_head = mono("skos:example", 20, GREY)
        ex_tags = m.VGroup(*[tag(s, 20, INK) for s in NATURES]).arrange(m.DOWN, buff=0.15, aligned_edge=m.RIGHT)
        examples = m.VGroup(ex_head, ex_tags).arrange(m.DOWN, buff=0.2, aligned_edge=m.RIGHT)
        examples.next_to(rn, m.LEFT, buff=0.9).align_to(rn, m.UP).shift(0.2 * m.UP)
        hook = m.DashedLine(rn.box.get_left(), examples.get_right() + 0.1 * m.RIGHT, dash_length=0.1,
                            stroke_width=2, color=GREY)
        self.play(m.Create(hook), m.FadeIn(ex_head), run_time=0.5)
        self.play(m.LaggedStart(*[m.FadeIn(t, shift=0.1 * m.RIGHT) for t in ex_tags], lag_ratio=0.3), run_time=1.6)
        classes = m.VGroup(sample, sr, rn, concept, c_has, c_rel, c_nat, c_sub, hook, examples)

        # --- an informative module, which imports SOSA
        until(self, v.at("informative"))
        rel_f = folder("Sample Relations", MODULE["sampling"], 5.4, 1.6, 26,
                       body=mono("http://www.w3.org/ns/sosa/sampling/", 18))
        sosa_f = folder("SOSA", MODULE["sosa_core"], 3.2, 1.6, 26)
        rel_f.move_to([-3.3, -0.3, 0])
        sosa_f.move_to([4.2, -0.3, 0])
        stamp = tag("informative", 24, GREY).next_to(rel_f, m.DOWN, buff=0.35)
        self.play(m.FadeOut(classes), run_time=0.6)
        self.play(m.FadeIn(rel_f, shift=0.1 * m.UP), m.FadeIn(stamp), run_time=0.9)
        until(self, v.at("imports"))
        imp = m.Arrow(rel_f.box.get_right(), sosa_f.box.get_left(), buff=0.15, stroke_width=3, color="#333333",
                      tip_shape=m.StealthTip)
        imp_l = mono("owl:imports", 20, GREY).next_to(imp, m.UP, buff=0.12)
        self.play(m.FadeIn(sosa_f, shift=0.1 * m.LEFT), m.GrowArrow(imp), m.FadeIn(imp_l), run_time=1.0)

        # --- the Turtle
        until(self, v.at("turtle"))
        ex = example_box(TURTLE, "Example · sample-relations.ttl (abridged)", 18)
        self.play(m.FadeOut(m.VGroup(rel_f, sosa_f, stamp, imp, imp_l)), run_time=0.5)
        ex.set(height=min(ex.height, 6.9)).move_to(0.2 * m.DOWN)
        self.play(m.FadeIn(ex, shift=0.2 * m.UP), run_time=0.8)
        self.play(ex.mark(5), run_time=0.3)
        until(self, v.at("brackets"))
        for i in range(8, 16):
            self.play(ex.mark(i), run_time=0.18)

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
