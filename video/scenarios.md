# Scenarios: one series, one episode per module

## The thread: "How do we know the Earth's atmosphere?"

Three examples of the spec share the same ultimate feature of interest,
`ex:EarthAtmosphere` (`skos:exactMatch` wikidata Q3230):

| example (file in `ssn/rdf/examples/`) | place | what is measured |
| --- | --- | --- |
| `historical-airtemp.ttl` | Hohe Warte station, Vienna (48.25° N, 16.36° E) | 22.5 °C, on 4 April 1872 at 15:00, mercury thermometer `ex:T99` |
| `bubble-provenance.ttl`, `paleo-atmosphere.ttl` | Antarctic ice sheet (73.35° S, 9.32° E) | an air bubble trapped at 15.202 m in an ice core: 240 ppm of CO₂, age 7,530 years |
| `LocatedSampling.ttl` | Saint-Étienne (45.44° N, 4.39° E) | an air sample |

Each episode starts from the planet, zooms down to a sensor or a sample,
draws the graph from it, and goes back up to the atmosphere. From one
episode to the next, viewers recognise the same globe and the same yellow
`ex:EarthAtmosphere` node. The identifiers on screen are those of the spec's
Turtle files: the video points to examples that viewers can open.

## Outline of an episode (2 to 4 min)

1. **Title card** — W3C + OGC, "SOSA/SSN · SOSA Observation" (style.md).
2. **The real world** — the globe turns, the camera dives towards the place;
   the place is line-drawn (station, borehole, building), then the sensor or
   the sample.
3. **From real to model** — each real thing becomes a node (see the three
   options proposed below).
4. **The graph builds up** — rectangles, identifiers, arrows leaving one
   rectangle and entering another; the camera tracks what grows.
5. **The zoom-out** — the `rdf:type` arrows rise towards a row of white
   classes: this is the module diagram, drawn the same way as in the spec.
6. **The Turtle** — a respec `.example` box, whose lines light up when the
   corresponding node or arrow flashes.
7. **End card** — the section URL, the repository, the comments list.

## The episodes

Status on 2026-10-20: episodes 1, 2 and 3 are done
(`episodes/01-introduction/`, `02-observation/`, `03-samples/`). No episode
announces the next one with "next time": they end with "Stay tuned for
more" (decided by Maxime Lefrançois on 2026-10-20).

### 1. Introduction: SOSA and SSN, the 2023 Edition as Candidate Recommendation (≈ 2 min 40) — **done**

The text follows the spec's Abstract and Introduction (Context, Scope, 2023
Edition). The globe and its sensors; "2.4, of what?": the river (the Danube
near Vienna), the current velocity, the sampling strategy; a thermostat for
actuation; the legend of the spec's colours
(Sensor/Actuator/Sampler → Observation/Actuation/Sampling → Procedure,
FeatureOfInterest/Sample, Property); SOSA within SSN (folders of the module
diagram, axioms); OGC, W3C, ETSI SAREF; the web graph and its uses; the
timeline 2017 → ISO 19156:2023 → 2023 Edition; the "W3C Candidate
Recommendation" stamp and the call for implementations; the cards of the
series. It replaces the former trailer (0); SOSA Common no longer has an
episode of its own: its terms (feature of interest, property, platform,
procedure) are introduced in episodes 2 to 4.

### 2. SOSA Observation: 4 April 1872, 15:00, Vienna (≈ 1 min 50) — **done**

The globe → Europe → Vienna → the line-drawn station → the shelter → the
thermometer. The mercury rises, a number appears: 22.5 °C. This number
becomes the grey result box; a `hasResult` arrow leaves it *backwards* and
gives birth to the purple observation `ex:SHW_T_1872-04-04T15`. From there,
one by one, with the camera following: `madeBySensor` → `ex:T99` (orange),
`observedProperty` → `ex:airTemperature` (green), `hasFeatureOfInterest` →
`ex:SHW` (yellow), `phenomenonTime`, `resultTime` (grey). Zoom-out:
`rdf:type` to the classes; the final figure is `Observation-overview.svg`.

### 3. SOSA Sampling: a 7,530-year-old air bubble (≈ 2 min 30) — **done**

The most spectacular, and the most geospatial. The globe rotates towards the
South Pole → the drilling site → the drill `ex:ThermalDrill2` (`Sampler`,
orange) → **vertical tracking shot** along the ice core `ex:IceCore12` down to
15.202 m → zoom on the bubble `ex:Bubble873`. The chain of samples is drawn
(`isSampleOf`), two observations leave the bubble (240 ppm, 7,530 years).
Then `hasUltimateFeatureOfInterest`: a long curved arrow leaves the frame;
the camera follows it, zooming out to the whole globe, where it lands in
`ex:EarthAtmosphere`. Full circle: from the globe to the bubble, from the
bubble to the globe.

### 4. SOSA Actuation (≈ 2 min 30)

The spec's example, `open-window.ttl` (`ex:window98`, `ex:closer-987`,
`ex:A188`), is at the scale of a building. Proposal: place it in
Saint-Étienne, at the location of `LocatedSampling.ttl`. The air sampled
outside (episode 3 in miniature) triggers the actuator that closes the
window: observation → decision → actuation, same graph shape, different verb
(`actsOnProperty`, `madeByActuator`). A more geospatial alternative, but
outside the spec's examples: a dam or irrigation valve.

### 5. SSN: the axioms behind the boxes (≈ 2 min 30)

The graph of episode 2, frozen. The OWL axioms appear on top of it: an arrow
splits into its inverse (`madeBySensor` / `madeObservation`), domain and
range colour the nodes by inference, the chain
`isSampleOf ∘ isSampleOf` justifies `isSampleOfUltimateFOI` (episode 3). An
inconsistent triple added on purpose turns red `#C00`. Message: SOSA can be
read on its own, SSN adds what is needed for reasoning.

### 6. System extension: capabilities and conditions (≈ 3 min)

An automatic weather station in Antarctica: it must survive −60 °C. The
ranges `NormalOperatingConditions`, `SuboptimalOperatingConditions`,
`SurvivableConditions` nest on a growing temperature scale; accuracy depends
on the context (`hasValidityContext`). The spec's example is the InkBird
sensor (`IBS-TH2-PLUS-capabilities.ttl`): choose between reusing it as is or
writing an Antarctic example.

### 7. OMS extension: collections and time series (≈ 3 min)

Back to Hohe Warte: the 1872 observation is not alone. Zoom-out: thousands
of observations stack up into an `ObservationCollection` that carries, once
and for all, what they share (sensor, property, feature); they fold into a
curve 1872 → today (`timeseries-oc.ttl`).

### 8. Samples extension (≈ 3 min)

The ice core is cut into sub-samples (`sample-relations.ttl`), the station
is a `SpatialSample` of the atmosphere, the samples are stored in a
`SampleCollection` (the laboratory freezer). The colours stay yellow: they
are all features.

### 9. Alignments: where the colours come from (≈ 2 min)

The PROV triangle (Entity, Activity, Agent, Plan); each vertex turns into
its SOSA counterpart (`sosa-prov.ttl`: `Execution ⊑ prov:Activity`,
`FeatureOfInterest ⊑ prov:Entity`, `Procedure ⊑ prov:Plan`…) while keeping
its colour. Then OGC SensorThings and OMS, SAREF, DUL as thumbnails.

## Three ways to go from real to model (to be chosen)

**A. Labelling.** Each real thing is surrounded by a dotted outline in the
colour of its category, and a mono label grows (`ex:T99`). The drawing
fades, the outlines remain: they are the nodes, which slide into the graph
layout (`ReplacementTransform`). Readable, safe, reusable in every episode.

**B. The overlay.** Split screen: the drawing on the left, the graph on the
right. A grey dashed line links each real thing to its node as the graph
grows. What each box denotes is visible at all times; needs more space.

**C. The box that swallows the world.** The camera zooms out; the real scene
shrinks until it fits in a rectangle, which becomes the node of the feature
of interest, with a thumbnail of the place inside. Strong for the feature of
interest and for `EarthAtmosphere` (the globe in a yellow box), less so for
the other nodes.

Proposal: **A** by default, **C** for features of interest (the real place
and the atmosphere).

## What this requires from manimgx (checked in the installed 0.1.1)

- `MovingCameraScene` and `self.camera.frame.animate.move_to(…)/.set(width=…)`:
  tracking and zoom; a × 1000 zoom-out (bubble → globe) is done in two
  steps, with a crossfade between two scales, since floating-point precision
  is limited.
- `GrowArrow`, `Arrow`, `DashedLine`, `CurvedArrow`, `ArcBetweenPoints`: the
  arrows leaving a rectangle; `DashedVMobject` for the dotted borders of
  individuals.
- `RoundedRectangle`, `Text` (Typst), `Code` or mono text for Turtle.
- `LaggedStart`, `TransformMatchingShapes`, `ReplacementTransform`,
  `Indicate`, `Circumscribe`, `ShowPassingFlash` (a pulse running along a
  chain of arrows).
- `ValueTracker` + `always_redraw`: the turning globe, the rising mercury,
  the time series curve.
- **The globe**: no texture (`TexturedSurface` is missing). Proposal: a
  vector globe in orthographic projection, drawn from the Natural Earth
  1:110m coastlines (public domain, downloaded into `data/`), recomputed at
  each frame by `always_redraw` — thin line, pale grey land, consistent with
  the flat respec style. A real 3D sphere (`ThreeDScene` + `Sphere`) is
  possible, but `inspect` does not check 3D layout.
- The fixed banner (section title, logos, URL): a separate layer, added by
  ffmpeg (style.md).
