"""The videos' globe: Natural Earth coastlines (public domain) in orthographic
projection, as line art, following the style (`video/style.md`, "The real world").

    from globe import Globe
    g = Globe(radius=3.4)
    lon, lat = m.ValueTracker(0), m.ValueTracker(20)
    earth = m.always_redraw(lambda: g.draw(lon.get_value(), lat.get_value()))
    self.play(lon.animate.set_value(16.36), lat.animate.set_value(48.25), run_time=4)
    g.point(lon0, lat0, 16.36, 48.25)      # Vienna, on screen

The GeoJSON files are in data/geo/ (downloaded from
github.com/nvkelso/natural-earth-vector, `geojson/`): ne_110m_land for the
whole globe, ne_50m_land and ne_50m_admin_0_boundary_lines_land when zooming in.
"""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path

import numpy as np

import manimgx as m

DATA = Path(__file__).resolve().parents[1] / "data" / "geo"
LAND_FILL = "#F2F2F2"
COAST = "#595959"
GRATICULE = "#D0D0D0"
HEADING = "#005A9C"


@cache
def _rings(name: str) -> list[np.ndarray]:
    """The rings (polygons) or lines of a GeoJSON, in degrees (lon, lat)."""
    gj = json.loads((DATA / f"{name}.geojson").read_text())
    out = []
    for f in gj["features"]:
        g = f["geometry"]
        if g["type"] == "Polygon":
            parts = [g["coordinates"]]
        elif g["type"] == "MultiPolygon":
            parts = g["coordinates"]
        elif g["type"] == "LineString":
            parts = [[g["coordinates"]]]
        elif g["type"] == "MultiLineString":
            parts = [g["coordinates"]]
        else:
            continue
        for poly in parts:
            for ring in poly[:1] if g["type"].endswith("Polygon") else poly:   # not the holes (lakes)
                out.append(np.radians(np.asarray(ring, float)))
    return out


def ortho(lonlat: np.ndarray, lon0: float, lat0: float) -> tuple[np.ndarray, np.ndarray]:
    """Orthographic projection (radius 1): (x, y) and the visibility cos c."""
    lam, phi = lonlat[:, 0], lonlat[:, 1]
    l0, p0 = np.radians(lon0), np.radians(lat0)
    cosc = np.sin(p0) * np.sin(phi) + np.cos(p0) * np.cos(phi) * np.cos(lam - l0)
    x = np.cos(phi) * np.sin(lam - l0)
    y = np.cos(p0) * np.sin(phi) - np.sin(p0) * np.cos(phi) * np.cos(lam - l0)
    return np.stack([x, y], 1), cosc


@cache
def river(*names: str) -> list[np.ndarray]:
    """The lines of a river from ne_50m_rivers_lake_centerlines, in radians (lon, lat).
    A river may carry several names there: the Danube is "Donau" upstream of
    Bratislava, "Danube" downstream."""
    gj = json.loads((DATA / "ne_50m_rivers_lake_centerlines.geojson").read_text())
    out = []
    for f in gj["features"]:
        if f["properties"].get("name") not in names:
            continue
        g = f["geometry"]
        for line in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
            out.append(np.radians(np.asarray(line, float)))
    return out


def sensor_points(n: int = 500, seed: int = 7) -> np.ndarray:
    """Sensors drawn at random over the whole sphere (lon, lat in degrees): the air,
    the oceans, the rivers and the soils."""
    rng = np.random.default_rng(seed)
    return np.column_stack([rng.uniform(-180, 180, n), np.degrees(np.arcsin(rng.uniform(-1, 1, n)))])


class Globe:
    def __init__(self, radius: float = 3.4, center=m.ORIGIN, detail: str = "110m", borders: bool = False,
                 graticule: float = 30) -> None:
        self.r, self.c = radius, np.asarray(center, float)
        self.land = f"ne_{detail}_land"
        self.borders = "ne_50m_admin_0_boundary_lines_land" if borders else None
        self.step = graticule

    def to_scene(self, xy: np.ndarray) -> np.ndarray:
        return np.column_stack([xy * self.r, np.zeros(len(xy))]) + self.c

    def point(self, lon0: float, lat0: float, lon: float, lat: float) -> np.ndarray:
        xy, _ = ortho(np.radians([[lon, lat]]), lon0, lat0)
        return self.to_scene(xy)[0]

    def _poly(self, ring: np.ndarray, lon0: float, lat0: float) -> np.ndarray | None:
        """A land polygon: hidden points are brought back onto the limb, at
        their azimuth, so that the fill stops at the globe's edge."""
        xy, cosc = ortho(ring, lon0, lat0)
        if (cosc < 0).all():
            return None
        hid = cosc < 0
        if hid.any():
            n = np.linalg.norm(xy[hid], axis=1, keepdims=True)
            xy[hid] = xy[hid] / np.maximum(n, 1e-9)
        return self.to_scene(xy)

    def _lines(self, line: np.ndarray, lon0: float, lat0: float) -> list[np.ndarray]:
        """A line (border, graticule) cut into its visible pieces."""
        xy, cosc = ortho(line, lon0, lat0)
        vis = cosc >= 0
        out, cur = [], []
        for p, v in zip(xy, vis):
            if v:
                cur.append(p)
            elif cur:
                out.append(np.array(cur)); cur = []
        if cur:
            out.append(np.array(cur))
        return [self.to_scene(s) for s in out if len(s) > 1]

    def sensors(self, lon0: float, lat0: float, pts: np.ndarray, opacity: float = 1.0,
                color: str = "#D79B00", radius: float = 0.035) -> m.VGroup:
        """The visible sensors, as dots in the systems' colour."""
        xy, cosc = ortho(np.radians(pts), lon0, lat0)
        return m.VGroup(*[m.Dot(p, radius=radius, color=color, fill_opacity=opacity)
                          for p in self.to_scene(xy[cosc > 0.05])])

    def river(self, names: tuple[str, ...], lon0: float, lat0: float, color: str = "#2A7FD4",
              width: float = 4) -> m.VGroup:
        out = m.VGroup()
        for line in river(*names):
            for seg in self._lines(line, lon0, lat0):
                out.add(m.VMobject(stroke_width=width, color=color).set_points_as_corners(seg))
        return out

    def draw(self, lon0: float, lat0: float, stroke: float = 1.6) -> m.VGroup:
        disc = m.Circle(radius=self.r, stroke_width=stroke * 1.4, color=COAST,
                        fill_color=m.WHITE, fill_opacity=1).move_to(self.c)
        grat = m.VGroup()
        t = np.radians(np.linspace(-180, 180, 181))
        for lat in np.arange(-90 + self.step, 90, self.step):
            for s in self._lines(np.column_stack([t, np.full_like(t, np.radians(lat))]), lon0, lat0):
                grat.add(m.VMobject(stroke_width=stroke * 0.6, color=GRATICULE).set_points_as_corners(s))
        u = np.radians(np.linspace(-90, 90, 91))
        for lon in np.arange(-180, 180, self.step):
            for s in self._lines(np.column_stack([np.full_like(u, np.radians(lon)), u]), lon0, lat0):
                grat.add(m.VMobject(stroke_width=stroke * 0.6, color=GRATICULE).set_points_as_corners(s))
        land = m.VGroup()
        for ring in _rings(self.land):
            p = self._poly(ring, lon0, lat0)
            if p is not None and len(p) > 2:
                land.add(m.Polygon(*p, stroke_width=stroke, color=COAST, fill_color=LAND_FILL, fill_opacity=1))
        out = m.VGroup(disc, grat, land)
        if self.borders:
            b = m.VGroup()
            for line in _rings(self.borders):
                for s in self._lines(line, lon0, lat0):
                    b.add(m.VMobject(stroke_width=stroke * 0.6, color=COAST).set_points_as_corners(s))
            out.add(b)
        return out
