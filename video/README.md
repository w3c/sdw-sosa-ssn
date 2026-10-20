# SOSA/SSN presentation videos

A series of narrated videos, one per module of the ontology: an off-screen
voice, manimgx animations that start from the planet and the real world
(places, sensors, samples, observations) and arrive at the graph that models
them, following the visual style of the W3C and OGC specifications. Branch
`manimgx`, opened on 2026-10-20.

| | |
| --- | --- |
| [scenarios.md](scenarios.md) | the geospatial thread, the episodes per module, the real → model transitions |
| [style.md](style.md) | the visual style guide: W3C (respec), OGC, spec colours |
| [charter.py](charter.py) | the style guide in Python: colours, nodes (`cls`, `ind`, `value`), arrows (`edge`), cards, `.example` box, `Voice` |
| [globe.py](globe.py) | the line-drawn globe (Natural Earth coastlines, orthographic projection) |
| [narration.yaml](narration.yaml) | the shared script: the narrator's voice and its tones |
| [cast.yaml](cast.yaml) | the cast: nobody on screen |
| [narrated.sh](narrated.sh) | one episode, from voice to MP4 |
| `episodes/<episode>/episode.yaml` | the scenario: lines and marks (`{do: mark, id, cue}`) |
| `episodes/<episode>/scene.py` | the manimgx scene, which waits for each mark |

Everything generated or downloaded goes into `data/` at the root of the
repository, ignored by git (`/data/` in `.gitignore`):

| | |
| --- | --- |
| `data/geo/` | Natural Earth coastlines and borders (GeoJSON, public domain) |
| `data/logos/w3c.svg` | the W3C logo of the TRs |
| `data/voices/narrator.wav`, `.txt` | the narrator's reference clip (a synthetic Qwen3-TTS VoiceDesign voice) and its transcript |
| `data/build/<episode>/` | voice (`lines/`, `audio.wav`), `timeline.json`, `animation.mp4`, `inspect` contact sheets |
| `data/build/video/voices/` | the voice cache (an unchanged line is not re-synthesised) |
| `data/<episode>.mp4` | the finished episode |

To download the data again:

```sh
mkdir -p data/geo data/logos
for f in ne_110m_land ne_50m_land ne_50m_admin_0_boundary_lines_land; do
  curl -sSfL -o data/geo/$f.geojson \
    https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/$f.geojson
done
curl -sSfL -o data/logos/w3c.svg https://www.w3.org/StyleSheets/TR/2021/logos/W3C
curl -sSfL -o data/geo/ne_50m_rivers_lake_centerlines.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_rivers_lake_centerlines.geojson
```

The narrator's reference clip, `data/voices/narrator.wav` (with its
transcript in `narrator.txt`), is not distributed: it is a synthetic voice,
generated once with Qwen3-TTS VoiceDesign from the description in
`narration.yaml`, then reused to clone every line with the same timbre.

## Making an episode

From the root of the repository:

```sh
video/narrated.sh video/episodes/02-observation/episode.yaml --dry         # estimated timing, inspect contact sheets
video/narrated.sh video/episodes/02-observation/episode.yaml               # voice, realignment, render → data/02-observation.mp4
video/narrated.sh video/episodes/02-observation/episode.yaml --scene-only  # the scene only, voice kept
```

`--dry` writes the contact sheets to `data/build/<episode>/`: look at them
before rendering. Synthesis and rendering use the graphics card: run outside
the sandbox (otherwise `no GPU adapter`).

## The pipeline

It relies on an external narration toolkit (`timeline.py`, `render.py`,
`castfile.py`), located by the `NARRATION_DIR` environment variable, and on
three Python environments given by `QWEN_PY`, `RENDER_PY` and `MANIMGX`
(see the header of `narrated.sh`). No character appears on screen:

1. `timeline.py` (`QWEN_PY`) synthesises the
   lines with Qwen3-TTS → `audio.wav`, `timeline.json`;
2. `render.py --align-only` (`RENDER_PY`) realigns each
   mark on the spoken word (Whisper);
3. `manimgx render` (`MANIMGX`), with the scene reading the
   times through `Voice().at(id)` and `until()` → `animation.mp4`;
4. ffmpeg lays `audio.wav` over the video, holding the last frame until the
   end of the voice → `data/<episode>.mp4`.

The voice leads, the animation follows: changing a line moves the times, and
the animation follows at the next render.

Three conventions with the toolkit:

- **Marks**: `timeline.py` keeps every gesture and its `cue`; a gesture
  `{do: mark, id: …, cue: word}` is only a named instant, which `Voice.at(id)`
  looks up. The character player is never launched.
- **Cast**: `castfile.py` requires a character; `cast.yaml` declares one,
  silent and never rendered. The narrator is a disembodied voice, declared in
  `narration.yaml`.
- **Paths**: the pipeline runs from `data/` (`COURSE_ROOT`), where
  `data/video` is a link to `video/`; its `build/` thus lands in
  `data/build/`.

## Decisions (decided by Maxime Lefrançois on 2026-10-20)

1. **Pilot: episode 2**, SOSA Observation at Hohe Warte
   ([scenarios.md](scenarios.md)).
2. **Real → model**: labelling (A) by default, the box that swallows the
   world (C) for features of interest.
3. **Audience**: vague knowledge of W3C, OGC and the Semantic Web. We say
   what an identifier, a triple, a class is, with no unexplained jargon; we
   do not assume viewers can read Turtle.
4. **A single voice**, off screen: a synthetic voice, cloned from one
   reference clip (`data/voices/narrator.wav`) for a constant timbre.
5. **Logos**: W3C and OGC, permission granted. The W3C logo is the TR one
   (`https://www.w3.org/StyleSheets/TR/2021/logos/W3C`), downloaded into
   `data/logos/`, without a frame; the OGC one is `ssn/images/OGC-0.png`.
6. **The address displayed everywhere** is `https://www.w3.org/TR/vocab-ssn-2023/`
   (`SPEC_URL` in `charter.py`), never the github.io one; the displayed
   status is "2023 Edition · W3C Candidate Recommendation" (`STATUS`).
7. **No "next time"** at the end of an episode: "Stay tuned for more".
