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

Status on 2026-10-30: the nine episodes are done (`episodes/01-introduction/` to
`09-alignments/`), all with the narrator's voice chosen by ear by Maxime Lefrançois
(seed 1598911631, README.md), and Turtle highlighted as in the spec
(`charter.example_box`, `box.mark(i)`). No episode
announces the next one with "next time": they end with "Stay tuned for
more" (decided by Maxime Lefrançois on 2026-10-20).

### 1. Introduction: SOSA and SSN, the 2023 Edition as Candidate Recommendation (≈ 3 min 10) — **done**

The text follows the spec's Abstract and Introduction (Context, Scope, 2023
Edition). The globe and its sensors; "2.4, of what?": the river (the Danube
near Vienna), the current velocity, the sampling strategy; a thermostat for
actuation; the legend of the spec's colours
(Sensor/Actuator/Sampler → Observation/Actuation/Sampling → Procedure,
FeatureOfInterest/Sample, Property); SOSA within SSN (folders of the module
diagram, axioms); OGC, W3C, ETSI SAREF; the web graph and its uses; the
timeline 2017 → ISO 19156:2023 → 2023 Edition; the "W3C Candidate
Recommendation" stamp and the call for implementations; the cards of the
series (those of episodes 7 to 9 follow the episodes as made, 2026-10-30). It replaces the former trailer (0); SOSA Common no longer has an
episode of its own: its terms (feature of interest, property, platform,
procedure) are introduced in episodes 2 to 4.

### 2. SOSA Observation: 4 April 1872, 15:00, Vienna (≈ 2 min 15) — **done**

The globe → Europe → Vienna → the line-drawn station → the shelter → the
thermometer. The mercury rises, a number appears: 22.5 °C. This number
becomes the grey result box; a `hasResult` arrow leaves it *backwards* and
gives birth to the purple observation `ex:SHW_T_1872-04-04T15`. From there,
one by one, with the camera following: `madeBySensor` → `ex:T99` (orange),
`observedProperty` → `ex:airTemperature` (green), `hasFeatureOfInterest` →
`ex:SHW` (yellow), `phenomenonTime`, `resultTime` (grey). Zoom-out:
`rdf:type` to the classes; the final figure is `Observation-overview.svg`.

### 3. SOSA Sampling: a 7,530-year-old air bubble (≈ 2 min 05) — **done**

The most spectacular, and the most geospatial. The globe rotates towards the
South Pole → the drilling site → the drill `ex:ThermalDrill2` (`Sampler`,
orange) → **vertical tracking shot** along the ice core `ex:IceCore12` down to
15.202 m → zoom on the bubble `ex:Bubble873`. The chain of samples is drawn
(`isSampleOf`), two observations leave the bubble (240 ppm, 7,530 years).
Then `hasUltimateFeatureOfInterest`: a long curved arrow leaves the frame;
the camera follows it, zooming out to the whole globe, where it lands in
`ex:EarthAtmosphere`. Full circle: from the globe to the bubble, from the
bubble to the globe.

### 4. SOSA Actuation: a window opens in Saint-Étienne (≈ 1 min 50) — **done**

The spec's example, `open-window.ttl` ("Simple Actuation to open a window",
chapter ModelFOI: `ex:window98`, `ex:openState`, `ex:closer-987`, `ex:A188`,
`hasSimpleResult true`), placed in Saint-Étienne, at the location of
`LocatedSampling.ttl`, on a simplified line drawing of the facade of the
École des Mines: the window is that of the director's office (right wing,
first floor). The globe with its sensors, then actuators (orange rings) →
Saint-Étienne → the facade → the window up close, its chain motor turning,
the sash opening (17:23 → 17:24). C for the window, A for the motor; the
graph of the actuation; then its classes side by side with those of the
observation (episode 2): the same shape, other verbs (`madeBySensor` /
`madeByActuator`, `observedProperty` / `actsOnProperty`); the
`ActuatingProcedure` and a rule. The spec's example opens the window (the
earlier proposal had it closing).

### 5. SSN: the axioms behind the boxes (≈ 1 min 55) — **done**

The graph of episode 2, read first with SOSA: definitions and hints
(`schema:domainIncludes`, `schema:rangeIncludes`), and the inverse that SOSA
already names (`madeBySensor` / `madeObservation`: inverses are in SOSA, not
SSN; chapter RDF-implementation, "Expressivity"). Then with SSN: suppose the
data only types the observation; the `owl:allValuesFrom` restrictions of
`ssn-observation.ttl` give the other nodes their category, and their colour,
by inference. The rules are local: `hasFeatureOfInterest` serves
observations, actuations and samplings, and SSN never uses `rdfs:domain` and
`rdfs:range`. Consistency: the collections are disjoint (`ssn.ttl`), and
`ex:collection-1`, said to be both, turns red `#C00`. SSN imports SOSA. (The
earlier idea of a chain `isSampleOf ∘ isSampleOf` is not in the ontology:
`hasUltimateFeatureOfInterest` only has a note about such a chain.)

### 6. System extension: capabilities and conditions (≈ 1 min 50) — **done**

An automatic weather station in Antarctica: it must survive −60 °C. The
ranges `NormalOperatingConditions`, `SuboptimalOperatingConditions`,
`SurvivableConditions` nest on a growing temperature scale; accuracy depends
on the context (`hasValidityContext`). The spec's example is the InkBird
sensor (`IBS-TH2-PLUS-capabilities.ttl`): **kept** (2026-10-30), so that the
identifiers on screen are those of files viewers can open; the episode opens
on the thermometer of Vienna, whose precision the data does not give.

### 7. OMS extension: collections and time series (≈ 1 min 45) — **done**

Back to Hohe Warte: the 1872 observation is not alone. Zoom-out: thousands
of observations stack up into an `ObservationCollection` that carries, once
and for all, what they share (sensor, property, feature); they fold into a
curve 1872 → today (`timeseries-oc.ttl`). Correction (2026-10-30): the
collections are in SOSA core, not in the OMS module; the episode shows them,
then OMS (ISO 19156:2023), the `ogc-ms:implements` links of `sosa-oms.ttl`
and the terms the module adds (non-normative). The curve is that of the
spec's example, four wind-speed values, not Vienna since 1872.

### 8. Sample Relations extension: what one arrow does not say (≈ 1 min 35) — **done**

The extension of the spec is Sample Relations (chapter Sample-Relations,
informative, namespace `sosa-rel:`), not the samples of OMS: the earlier
proposal (sub-samples of the ice core, a `SpatialSample`, a `SampleCollection`)
is replaced by the spec's example, `sample-relations.ttl`. The `isSampleOf`
arrow of episode 3 (`ex:Bubble873` → `ex:IceCore12`) does not say how: split,
crushed, a station along a traverse, a pixel within an image? The arrow
becomes a node, `SampleRelationship`, with its related sample and its
nature. Then the example: the rock specimen `relex:CSRWA25569`, cut and set
in a polished resin mount (`-mount7`, `isSampleOf` the specimen), and spot 1
under a microprobe, whose relationship points to the mount with the nature
"probe spot on polished mount". C for the three samples. The classes of the
module, `RelationshipNature` ⊑ `skos:Concept` and its `skos:example`; the
module imports SOSA. The rock, the mount and the probe are an illustration:
the example only gives labels.

### 9. Alignments: where the colours come from (≈ 2 min) — **done**

The colour key of the spec's diagrams, which the chapter Notation calls
"similar" to that of PROV-O (activities are blue there, purple here): the
PROV classes in PROV-O's own notation (Activity, Entity, Agent, Plan), and
each category under its PROV class (`sosa-prov.ttl`: `Execution ⊑
prov:Activity`, `System ⊑ prov:Agent ⊔ prov:Entity`, `FeatureOfInterest`,
`Sample`, `Property ⊑ prov:Entity`, `Procedure ⊑ prov:Plan`); the arrows
`isSampleOf ⊑ prov:wasDerivedFrom` and `hasResult ⊑ prov:generated` on the
graphs of episodes 3 and 2. Then the other alignments, in the chapter's three
groups, each card giving what becomes of `sosa:FeatureOfInterest` there: DUL,
DOLCE, BFO · CCO, PROV-O; SAREF, IDO (Industrial Data Ontology, ISO 23726-3),
OBOE; SensorThings and Connected Systems, where the alignment is a table. The
SSSOM spreadsheet `sosa-mappings-sssom.xlsx` and its rows for
`sosa:FeatureOfInterest`. The schema.org alignment (`sosa-sdo.ttl`) has no
chapter: it is not shown.

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
