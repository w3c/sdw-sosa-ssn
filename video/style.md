# Visual style guide

The goal: viewers should recognise a W3C/OGC specification at first glance,
not a lecture. Three sources, in this order of priority:

1. **the spec's diagrams** (`ssn/chapters/Notation.html`,
   `ssn/images/Notation-ClassKey.svg`) for everything graph-related;
2. **the W3C TR stylesheet** (`https://www.w3.org/StyleSheets/TR/2021/base.css`,
   the one respec loads) for the page, headings and boxes;
3. **the OGC logo** for the OGC accent.

## The frame

- 1920 × 1080, 25 fps (the format of the narrated pipeline).
- White background, black ink: like the spec, and like the diagrams.
- Font: `sans-serif` in the W3C CSS; we use **Noto Sans** (installed, and
  the one of the w3.org site). Code and identifiers: **DejaVu Sans Mono**
  (in the `Menlo, Consolas, "DejaVu Sans Mono"` stack of the CSS).

## Page colours (TR 2021 CSS)

| role | colour | use in the video |
| --- | --- | --- |
| h1–h3 headings | `#005A9C` | scene title, section number |
| links | `#034575`, underline `#707070` | footer URL, clickable term names |
| table of contents background | `#F7F8F9` | side banner or chapter card |
| W3C logo | `#1A5E9A` (active: `#C00`) | title card |
| active / error | `#C00` | the only wrong thing on screen |
| OGC (sampled from `OGC-0.png`) | ≈ `#0070C8` | title card, OGC rule |

The respec boxes, thick left border and pale background:

| box | border | background | title |
| --- | --- | --- | --- |
| `.note` | `#52E052` | `#E9FBE9` | `hsl(120,70%,22%)` |
| `.example` | `#E0CB52` | `#FCFAEE` | `#574B0F` |
| `.issue` | `#E05252` | `#FBE9E9` | `#831616` |

`.example` is used for Turtle on screen, `.note` for a remark by the voice
that should stay readable.

## The graph: the spec's notation

Taken as is from `Notation-ClassKey.svg` (colours aligned with PROV-O,
branch `515-prov-colours`, merged):

| category | fill | border | PROV equivalent |
| --- | --- | --- | --- |
| Execution (Observation, Actuation, Sampling) or Deployment | `#E1D5E7` | `#9673A6` | `prov:Activity` |
| Procedure | `#F8CECC` | `#B85450` | `prov:Plan` |
| System (Sensor, Actuator, Sampler) or Platform | `#FFE6CC` | `#D79B00` | `prov:Agent` |
| FeatureOfInterest or Sample | `#FFFF88` | `#36393D` | `prov:Entity` |
| Property | `#D5E8D4` | `#82B366` | `prov:Entity` |
| Value (literal, quantity, time) | `#EEEEEE` | `#36393D` | — |
| individual without a category | `#CCE5FF` | `#36393D` | — |
| class | `#FFFFFF` | `#000000` | — |
| context (described elsewhere) | `#FFFFFF` | `#999999`, grey text | — |

The grammar:

- **class**: white rectangle, solid black line, name in Noto Sans
  (`Observation`); unprefixed names are in `sosa:`;
- **individual**: rectangle filled with its category colour, **dotted
  border**, identifier in mono (`ex:observation-1a`), label below if
  needed;
- **property between classes**: solid arrow, italic label;
- **property between individuals**: **dashed** arrow, italic label;
- **`rdf:type`**: dashed arrow to the class, labelled `rdf:type`;
- **subclass**: solid line, open triangle arrowhead;
- **modules** (module diagrams): folders, `#FFF2CC`/`#D6B656` and
  `#E1D5E7`/`#9673A6`, dependencies dashed.

## The real world

It must stay on the same page as the graph: no photos, no realistic
rendering, line drawing only.

- **the globe**: orthographic projection, Natural Earth 1:110m coastlines in
  `#595959` lines, land `#F2F2F2`, white sea, graticule `#D0D0D0`; the
  episode's location marked with a `#005A9C` dot;
- **places and objects** (station, shelter, thermometer, drill, core,
  window): thin black line, pale grey fills; the only colour is that of the
  SOSA category, which appears when the thing becomes a node;
- **physical quantities** (mercury, ice, bubble): grey and blue `#005A9C`
  as a light fill, never the category colours.

## Layout

- **Title card**: like the header of a TR — W3C and OGC logos at top left,
  title "Semantic Sensor Network Ontology" in `#005A9C`, status
  ("W3C Editor's Draft"), editors, URL `w3c.github.io/sdw-sosa-ssn/ssn/` as a
  `#034575` link.
- **Chapter card**: an `h2` of the spec, number included ("4. Observations"),
  in `#005A9C`, on a white background, with a thin rule below.
- **During an animation**: a fixed banner (section title at top left, small
  logos at bottom right, section URL at bottom left). The banner does not
  move when the camera moves: `pin()` in `charter.py` makes it follow the
  frame (`add_fixed_in_frame_mobjects` does not do it in a 2D scene in
  manimgx 0.1.1).
- **Zooming on a map** enlarges the map itself, not the camera: a camera
  zoom thickens the lines by the same factor.
- **End card**: the links (spec, GitHub repository, `public-sdw-comments`
  list), the two logos.
