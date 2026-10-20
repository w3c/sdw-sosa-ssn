#!/usr/bin/env bash
# One episode: the off-screen voice and the manimgx animation, in one MP4. No
# character on screen. The narration toolkit (timeline.py, render.py, castfile.py)
# is an external tool, located by NARRATION_DIR; render.py is used only to
# realign the words on the audio.
#
#   video/narrated.sh video/episodes/02-observation/episode.yaml          everything, up to data/02-observation.mp4
#   video/narrated.sh video/episodes/02-observation/episode.yaml --dry    estimated timings without voice, then
#                                                                         `manimgx inspect`: the layout
#   video/narrated.sh … --scene-only                                      the scene and sound, without redoing the voice
#
# Everything produced goes into data/ (ignored by git): data/build/<episode>/
# (voice, timeline.json, animation.mp4), the voice cache (data/build/video/voices),
# and the final MP4 data/<episode>.mp4. The pipeline runs from data/, where
# data/video is a link to video/.
#
# Steps: timeline.py (Qwen3-TTS); render.py --align-only (Whisper realigns
# each `cue`); manimgx render, the scene reading timeline.json via
# NARRATION_TIMELINE; ffmpeg puts audio.wav onto the video.
#
# Environment (no default: set them for your machine):
#   NARRATION_DIR  directory of the narration toolkit (timeline.py, render.py)
#   QWEN_PY        Python with Qwen3-TTS (speech synthesis)
#   RENDER_PY      Python with faster-whisper and PyYAML (word alignment)
#   MANIMGX        the manimgx executable
set -euo pipefail

REPO=$(cd "$(dirname "$0")/.." && pwd)
: "${NARRATION_DIR:?set NARRATION_DIR}" "${QWEN_PY:?set QWEN_PY}" "${RENDER_PY:?set RENDER_PY}" "${MANIMGX:?set MANIMGX}"
NARRATION=$NARRATION_DIR

SC=$(realpath --relative-to="$REPO" "$1"); shift
MODE=${1:-}
[[ -n $MODE ]] && shift
DATA=$REPO/data
mkdir -p "$DATA"
ln -sfn ../video "$DATA/video"
cd "$DATA"
export COURSE_ROOT=$DATA

key() { "$RENDER_PY" -c "import sys, yaml; print(yaml.safe_load(open(sys.argv[1]))[sys.argv[2]])" "$SC" "$1"; }
NAME=$(basename "$(dirname "$SC")")
OUT=build/$NAME
SCENE=$(key scene)
VIDEO=$(key video)
export NARRATION_TIMELINE=$DATA/$OUT/timeline.json
quiet() { grep -v -E "pad_token|SoX|sox|\*\*\*|sourceforge|path variables|Fetching|^\s*$" >&2 || true; }

# manimgx writes its storyboard next to the scene: we give it the scene
# through a link in data/, so that nothing generated goes into video/
mkdir -p "$OUT"
ln -sfn "$DATA/$SCENE" "$OUT/scene.py"

if [[ $MODE == --dry ]]; then
  "$QWEN_PY" "$NARRATION/timeline.py" "$SC" "$OUT" --dry 2> >(quiet)
  "$MANIMGX" inspect "$OUT/scene.py" "$@"
  exit
fi

if [[ $MODE != --scene-only ]]; then
  "$QWEN_PY" "$NARRATION/timeline.py" "$SC" "$OUT" 2> >(quiet)
  "$RENDER_PY" "$NARRATION/render.py" "$SC" "$OUT" --align-only
fi
mkdir -p "$(dirname "$VIDEO")"
"$MANIMGX" render "$OUT/scene.py" -o "$DATA/$VIDEO"

# manimgx writes no sound, and its stream stops at the last frame that
# changes: tpad holds that frame until the end of the voice
D=$("$RENDER_PY" -c "import json,sys; print(json.load(open(sys.argv[1]))['audio_end'])" "$NARRATION_TIMELINE")
ffmpeg -v error -y -i "$VIDEO" -i "$OUT/audio.wav" \
  -filter_complex "[0:v]fps=25,tpad=stop_mode=clone:stop_duration=3600[v]" -map "[v]" -map 1:a \
  -t "$D" -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 160k "$NAME.mp4"
echo "$DATA/$NAME.mp4"
