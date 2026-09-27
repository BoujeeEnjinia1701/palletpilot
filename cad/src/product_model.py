"""PalletPilot product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the retrofit kit on a donor manual pallet jack:
a charcoal drive module subframe with filleted plate, trailing cheeks, axle caps, bolt heads and
coil preload springs; two hub motor wheels with grooved treads and machined hub faces; a teal
folded aluminium enclosure with side louvers, a charcoal lid frame and a clear polycarbonate
window over the LiFePO4 pack, motor driver, contactors and controller; a rear emergency stop on
its yellow plate, a red battery disconnect knob, cable glands and a name plate; the manual release
lever; a steel U hoop carrying a black safety edge, with white UWB anchor radomes on its corners;
the obstacle lidar puck on its bracket; and a tiller control head with rubber grips, thumbwheel
throttles, belly-reverse paddle, key switch, horn button, emergency stop, UWB anchor and a lit
amber beacon (walk mode), joined to the enclosure by a spiral-wrapped cable. Context is the donor
jack, a 48 x 40 in stringer pallet with cartons, and the shared clay mannequin holding the tiller
with the operator's UWB belt tag.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research prototype, not a certified industrial truck.

Every main dimension and interface comes from PARAMS and derived() in model.py. Axes as model.py:
fork tips toward -X, drive end toward +X, Y across the forks, Z up from the floor. Differences
from model.py (see docs/REVIEW.md, session 2026-09-26): the handle is drawn at HANDLE_DEG (40 deg
from vertical, mid walk band) instead of the 20 deg that model.py shows, so the operator's hands
meet the grips at a natural height; the tiller head grips span GRIP_SPAN over their end caps
against the 220 mm head_w; and the tiller's UWB anchor sits under the left grip instead of 35 mm
outboard of the head. The operator tag (BOM 15) and the spiral-wrapped tiller cable (BOM 17),
which model.py does not model, are shown.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Axis, Box, Cylinder, Ellipse, Location, Plane, Pos, RegularPolygon, Rot, Solid,
                       Sphere, Torus, Vector, extrude, fillet)
from model import PARAMS, derived

TITLE = "PalletPilot: powered follow-me retrofit kit for a manual pallet jack"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 24, "az": -40,
     "note": "Product render from the front right and above (about 24 deg elevation); drive end at right, "
             "operator walking behind the load holding the tiller"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): subframe, hub motors, "
             "enclosure and electronics, bumper, UWB anchors, lidar, tiller head, tag"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 26, "az": -34,
     "note": "Detail from the front right and above (about 26 deg elevation): drive module, enclosure with "
             "electronics behind the clear lid, lidar, bumper and UWB anchors"},
]

HANDLE_DEG = 40.0            # handle angle from vertical shown in the renders (walk band 20 to 70 deg)
GRIP_Y = (46.0, 118.0)       # grip sleeve inner and outer Y on each side of the tiller head
GRIP_SPAN = 2 * (GRIP_Y[1] + 6.0)
PERSON_H = 1750.0

# Colours (restrained product palette; kit accent)
C_ACCENT = "#0F766E"
C_ACCENT2 = "#115E59"
C_CHAR = "#2B2F36"
C_BLACK = "#1C1F24"
C_RUBBER = "#202327"
C_METAL = "#B8BEC6"
C_ZINC = "#9EA5AE"
C_WHITE = "#E9EAEC"
C_LABEL = "#F4F4F2"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RELAY = "#1E3A5F"
C_PACK = "#34506B"
C_COPPER = "#B87333"
C_RED = "#C81E1E"
C_YELLOW = "#E8B10E"
C_AMBER = "#F59E0B"
C_DONOR = "#707781"
C_DONOR2 = "#565C66"
C_WOOD = "#C8A97E"
C_KRAFT = "#C9A77A"
C_TAPE = "#B89466"
C_CLAY = "#9CA3AF"
C_FABRIC = "#2A2E35"


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, c, r):
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _ymax(s):
    return s.faces().sort_by(Axis.Y)[-1].edges()


def _ymin(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_y(x, y, z, af, h):
    """Hex prism along Y centred at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Pos(0, 0, -h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Pos(0, 0, -h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _wheel_parts(x, y, z, r, w, side):
    """Hub motor wheel, axle along Y; side = +1 or -1 (outboard face toward side * Y)."""
    tire = _ycyl(x, y, z, r, w)
    tire = _fillet_try(tire, tire.edges(), [9.0, 6.0, 3.0])
    for dy in (-14.0, 0.0, 14.0):
        tire -= _ycyl(x, y + dy, z, r + 1, 3.5) - _ycyl(x, y + dy, z, r - 3.0, 5)
    tire -= _ycyl(x, y + side * (w / 2 - 3), z, r - 22, 8) + _ycyl(x, y - side * (w / 2 - 3), z, r - 22, 8)
    hub = _ycyl(x, y, z, r - 23, w - 4)
    hub = _fillet_try(hub, hub.edges(), [3.0, 1.5])
    face = y + side * (w / 2 - 2)
    hub += _ycyl(x, face + side * 1.5, z, 34, 3)
    hub = _fillet_try(hub, (_ymax(hub) if side > 0 else _ymin(hub)), [1.2, 0.6])
    bolts = []
    for k in range(6):
        a = math.radians(30 + 60 * k)
        bolts.append(_hex_y(x + 52 * math.cos(a), face + side * 1.5, z + 52 * math.sin(a), 8.0, 3.0))
    inner = y - side * (w / 2 - 2)
    cable = _ycyl(x + 20, inner - side * 6, z - 30, 6, 14)
    return tire, hub, _union(bolts), cable


# ------------------------------------------------------------------ main
def product_parts(P=PARAMS):
    from context_parts import mannequin, mannequin_landmarks
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    kx = P["kingpin_x"]
    a = math.radians(HANDLE_DEG)
    L = P["handle_len"]
    tx, tz = kx + L * math.sin(a), P["pivot_z"] + L * math.cos(a)      # handle top at the render angle

    # ============================================================ donor jack (context, no BOM)
    fy = P["out_w"] / 2 - P["fork_w"] / 2
    ft, fl, fw, fh, xt = P["fork_top"], P["fork_len"], P["fork_w"], P["fork_h"], P["x_tip"]
    forks = []
    for s in (-1, 1):
        o = _box(xt, xt + fl, s * fy - fw / 2, s * fy + fw / 2, ft - fh, ft)
        o = _fillet_try(o, _par(o, Axis.X), [6.0, 4.0])
        o -= _box(xt - 1, xt + fl + 1, s * fy - fw / 2 + 5, s * fy + fw / 2 - 5, ft - fh - 1, ft - 5)
        forks.append(o)
    frame = _box(-60, 40, -P["out_w"] / 2, P["out_w"] / 2, 25, 230)
    frame = _fillet_try(frame, _par(frame, Axis.Y), [14.0, 10.0])
    frame -= _box(-45, 41, -P["out_w"] / 2 + 185, P["out_w"] / 2 - 185, 24, 150)
    rollers = _ycyl(P["load_roller_x"], fy, 40, 40, 110) + _ycyl(P["load_roller_x"], -fy, 40, 40, 110)
    add("Donor jack forks and frame (not in kit)", _union(forks) + frame, C_DONOR, "painted", None, "context", (0, 0, 0))
    add("Donor load rollers", rollers, C_RUBBER, "rubber", None, "context", (0, 0, 0))

    pump = _zcyl(kx, 0, 250, 55, 200)
    pump = _fillet_try(pump, _top(pump), [8.0, 5.0])
    pump += _zcyl(kx, 0, 145, 42, 12)
    yoke = _box(kx - 50, kx + 50, -110, 110, 150, P["yoke_top"])
    yoke = _fillet_try(yoke, _par(yoke, Axis.Z), [12.0, 8.0])
    add("Donor pump and steering yoke", pump + yoke, C_DONOR2, "painted", None, "context", (0, 0, 0))
    ram = _zcyl(kx, 0, 362, 20, 24)
    add("Donor pump ram (chrome)", ram, C_METAL, "metal", None, "context", (0, 0, 0))
    steer = []
    for s in (-1, 1):
        w_ = _ycyl(kx, s * P["steer_y"], P["steer_r"], P["steer_r"], P["steer_w"])
        steer.append(_fillet_try(w_, w_.edges(), [8.0, 5.0]))
    add("Donor steer wheels", _union(steer), C_RUBBER, "rubber", None, "context", (0, 0, 0))

    # handle: clevis at the pivot, tube to the tiller head
    hdir = Vector(math.sin(a), 0, math.cos(a))
    piv = Vector(kx, 0, P["pivot_z"])
    shaft = _rod(tuple(piv), tuple(piv + hdir * (L - 50)), P["handle_r"])
    clevis = _box(kx - 30, kx + 30, -45, 45, P["pivot_z"] - 20, P["pivot_z"] + 25)
    clevis = _fillet_try(clevis, _par(clevis, Axis.Y), [10.0, 6.0])
    add("Donor handle", shaft + clevis, C_DONOR, "painted", None, "context", (0, 0, 0))
    add("Donor handle pivot pin", _ycyl(kx, 0, P["pivot_z"], 10, 110), C_METAL, "metal", None, "context", (0, 0, 0))

    # pallet and load (context)
    PX0, PX1 = -1225.0, -5.0
    boards = [_box(x0, x0 + 98, -508, 508, 124, 140) for x0 in [PX0 + i * (PX1 - PX0 - 98) / 6 for i in range(7)]]
    boards += [_box(x0, x0 + 98, -508, 508, 0, 14) for x0 in (PX0, (PX0 + PX1) / 2 - 49, PX1 - 98)]
    stringers = [_box(PX0, PX1, y - 19, y + 19, 14, 124) for y in (-489, 0, 489)]
    add("Pallet, 48 x 40 in stringer", _union(boards + stringers), C_WOOD, "wood", None, "context", (0, 0, 0))
    cartons, tape = [], []
    cw_, cd_, ch_ = (PX1 - PX0 - 20) / 3, 1000.0 / 2, 270.0
    for i in range(3):
        for j in range(2):
            for k in range(2):
                x0 = PX0 + 10 + i * cw_
                y0 = -500 + j * cd_
                z0 = 140 + k * ch_
                c = _box(x0 + 2, x0 + cw_ - 2, y0 + 2, y0 + cd_ - 2, z0, z0 + ch_ - 2)
                c = _fillet_try(c, c.edges(), [3.0, 1.5])
                cartons.append(c)
                if k == 1:
                    tape.append(_box(x0 + cw_ / 2 - 25, x0 + cw_ / 2 + 25, y0 + 2, y0 + cd_ - 2,
                                     z0 + ch_ - 2, z0 + ch_ - 1.4))
    add("Cartons, about 1,000 kg", _union(cartons), C_KRAFT, "paper", None, "context", (0, 0, 0))
    add("Carton tape", _union(tape), C_TAPE, "paper", None, "context", (0, 0, 0))

    # ============================================================ 1 drive module subframe
    t = P["plate_t"]
    hy = P["drive_track"] / 2 + P["drive_w"] / 2 + 5
    ES = (0, 0, 0)
    plate = _box(P["plate_x0"], P["plate_x1"], -P["plate_half_w"], P["plate_half_w"], P["plate_z"], P["plate_z"] + 20)
    plate = _fillet_try(plate, _par(plate, Axis.Z), [16.0, 10.0])
    plate = _fillet_try(plate, _top(plate), [2.0, 1.0])
    clamp = _box(P["plate_x0"], P["plate_x0"] + 20, -40, 40, 140, P["plate_z"]) + _box(kx + 10, P["plate_x0"], -40, 40, 140, 150)
    cheeks = []
    for s in (-1, 1):
        y0, y1 = (hy, hy + 2 * t) if s > 0 else (-hy - 2 * t, -hy)
        c = _box(P["cheek_x0"], P["cheek_x1"], y0, y1, 70, P["plate_z"])
        c = _fillet_try(c, [e for e in _par(c, Axis.Y) if e.center().Z < 100], [45.0, 30.0, 15.0])
        cheeks.append(c)
    sub = plate + clamp + _union(cheeks)
    add("Drive module subframe", sub, C_CHAR, "painted", 1, "shell", ES)

    bolts = []
    for x in (P["plate_x0"] + 8, P["plate_x1"] - 12):
        for s in (-1, 1):
            bolts.append(_hex_z(x, s * 166, P["plate_z"] + 23, 13.0, 6.0))
    for s in (-1, 1):
        bolts.append(_hex_z(P["plate_x0"] + 10, s * 25, 137, 13.0, 6.0))
        cap_y = s * (hy + 2 * t + 4)
        bolts.append(_hex_y(P["drive_x"], cap_y, P["drive_r"], 24.0, 8.0))
        bolts.append(_ycyl(P["drive_x"], s * (hy + 2 * t + 9), P["drive_r"], 7, 3))
    add("Subframe bolts and axle nuts", _union(bolts), C_ZINC, "metal", 1, "shell", ES)

    springs, cups = [], []
    for s in (-1, 1):
        sx, sy = P["drive_x"] - 70, s * (hy + 30)
        cups.append(_zcyl(sx, sy, 200, 22, 10) + _zcyl(sx, sy, 162, 22, 6))
        cups.append(_box(sx - 22, sx + 22, min(sy, s * hy), max(sy, s * hy), 157, 165))
        for k in range(5):
            springs.append(Pos(sx, sy, 170 + 6.5 * k) * Torus(15.0, 2.8))
    add("Preload spring seats", _union(cups), C_CHAR, "painted", 1, "shell", ES)
    add("Preload springs", _union(springs), C_ACCENT, "painted", 1, "shell", ES)

    # ============================================================ 2 hub motors
    r, dx, dy = P["drive_r"], P["drive_x"], P["drive_track"] / 2
    for s, nm in ((1, "right"), (-1, "left")):
        tire, hub, hb, cab = _wheel_parts(dx, s * dy, r, r, P["drive_w"], s)
        EM = (0, s * 300, 0)
        add(f"Hub motor tyre, {nm}", tire, C_RUBBER, "rubber", 2, "shell", EM)
        add(f"Hub motor housing, {nm}", hub, C_METAL, "metal", 2, "shell", EM)
        add(f"Hub motor face bolts, {nm}", hb, C_CHAR, "metal", 2, "shell", EM)
        add(f"Hub motor cable exit, {nm}", cab, C_BLACK, "plastic", 2, "shell", EM)

    # ============================================================ 3 enclosure, lid and window
    ex0, ex1, ey, ez0, etop = P["enc_x0"], P["enc_x1"], P["enc_half_w"], P["enc_z0"], P["enc_top"]
    et = P["enc_t"] * 2
    lid_t = 6.0
    EE = (0, 0, 200)
    body_o = _box(ex0, ex1, -ey, ey, ez0, etop - lid_t)
    body_o = _fillet_try(body_o, _par(body_o, Axis.Z), [12.0, 8.0])
    body_o = _fillet_try(body_o, _bottom(body_o), [3.0, 2.0])
    body = body_o - _box(ex0 + et, ex1 - et, -ey + et, ey - et, ez0 + et, etop)
    for s in (-1, 1):                                     # louvers on both long sides
        for k in range(6):
            x = ex0 + 150 + 18 * k
            body -= _box(x - 3.5, x + 3.5, s * ey - 3, s * ey + 3, 272, 300)
    add("Battery and electronics enclosure", body, C_ACCENT, "painted", 3, "shell", EE)
    seam = _box(ex0 + 12, ex1 - 12, -ey - 0.5, ey + 0.5, etop - lid_t - 1.2, etop - lid_t) - \
        _box(ex0 + 3, ex1 - 3, -ey + 2, ey - 2, etop - lid_t - 2, etop)
    seam += _box(ex0 - 0.5, ex1 + 0.5, -ey + 12, ey - 12, etop - lid_t - 1.2, etop - lid_t) - \
        _box(ex0 + 2, ex1 - 2, -ey - 1, ey + 1, etop - lid_t - 2, etop)
    add("Enclosure lid gasket line", seam, C_BLACK, "rubber", 3, "shell", (0, 0, 740))

    lid_o = _box(ex0, ex1, -ey, ey, etop - lid_t, etop)
    lid_o = _fillet_try(lid_o, _par(lid_o, Axis.Z), [12.0, 8.0])
    lid_o = _fillet_try(lid_o, _top(lid_o), [2.5, 1.5])
    wx0, wx1, wy = ex0 + 24, ex1 - 24, ey - 24
    win_cut = _box(wx0, wx1, -wy, wy, etop - lid_t - 1, etop + 1)
    win_cut = _fillet_try(win_cut, _par(win_cut, Axis.Z), [8.0, 5.0])
    lid = lid_o - win_cut
    add("Enclosure lid frame", lid, C_CHAR, "painted", 3, "shell", (0, 0, 760))
    pane = _box(wx0 - 4, wx1 + 4, -wy - 4, wy + 4, etop - 3.5, etop - 0.5)
    pane = _fillet_try(pane, _par(pane, Axis.Z), [10.0, 6.0])
    add("Clear polycarbonate lid window", pane, C_WINDOW, "clear", 3, "shell", (0, 0, 800))
    screws = []
    for x in (ex0 + 12, (ex0 + ex1) / 2, ex1 - 12):
        for s in (-1, 1):
            sc = _zcyl(x, s * (ey - 12), etop + 0.8, 3.6, 1.6)
            sc -= _box(x - 2.2, x + 2.2, s * (ey - 12) - 0.5, s * (ey - 12) + 0.5, etop + 0.8, etop + 2)
            screws.append(sc)
    add("Lid screws", _union(screws), C_METAL, "metal", 17, "shell", (0, 0, 830))

    # name plate and marking on the rear (+X) face, facing the operator
    plate_n = _box(ex1, ex1 + 0.6, 10, 120, 282, 302)
    add("Name plate", plate_n, C_LABEL, "paper", 3, "shell", EE)
    ink = _box(ex1 + 0.6, ex1 + 0.9, 20, 88, 290, 296) + _box(ex1 + 0.6, ex1 + 0.9, 94, 112, 288, 298)
    add("Name plate print", ink, C_ACCENT2, "paper", 3, "shell", EE)
    warn = _box(ex1, ex1 + 0.6, 10, 120, 238, 250)
    add("Lithium battery warning label", warn, C_YELLOW, "paper", 3, "shell", EE)

    # glands: rear face (motor and bumper cables), lid (tiller cable)
    gl = []
    for y in (100.0, 130.0):
        g = _hex_x(ex1 + 2.5, y, 262, 20.0, 5.0) + _xcyl(ex1 + 9, y, 262, 8.0, 8.0)
        gl.append(g)
    for s in (-1, 1):
        gl.append(_hex_y(ex0 + 40, s * (ey + 2.5), 250, 20.0, 5.0) + _ycyl(ex0 + 40, s * (ey + 9), 250, 8.0, 8.0))
    add("Enclosure cable glands", _union(gl), C_BLACK, "plastic", 17, "shell", EE)

    # ============================================================ 4 to 7 internals
    z0 = ez0 + et
    EI = (0, 0, 420)
    pack = _box(ex0 + 8, ex0 + 8 + P["pack_w"], -P["pack_l"] / 2, P["pack_l"] / 2, z0, z0 + P["pack_h"] - 6)
    pack = _fillet_try(pack, pack.edges(), [6.0, 4.0, 2.0])
    add("LiFePO4 pack 25.6 V 20 Ah (shrink wrapped)", pack, C_PACK, "plastic", 4, "internal", EI)
    pz = z0 + P["pack_h"] - 6
    bms = _box(ex0 + 20, ex0 + 8 + P["pack_w"] - 12, -95, 20, pz, pz + 2)
    add("Pack BMS board", bms, C_PCB, "plastic", 4, "internal", EI)
    bmsc = _box(ex0 + 30, ex0 + 60, -80, -40, pz + 2, pz + 5) + _box(ex0 + 70, ex0 + 100, -80, -50, pz + 2, pz + 4) \
        + _box(ex0 + 40, ex0 + 90, -20, 10, pz + 2, pz + 5)
    add("BMS components", bmsc, C_CHIP, "plastic", 4, "internal", EI)
    bus = _box(ex0 + 24, ex0 + 104, 40, 52, pz, pz + 1.5) + _box(ex0 + 24, ex0 + 104, 90, 102, pz, pz + 1.5)
    add("Pack busbars", bus, C_COPPER, "metal", 4, "internal", EI)
    lab4 = _box(ex0 + 30, ex0 + 100, 106, 128, pz, pz + 0.4)
    add("Pack label", lab4, C_LABEL, "paper", 4, "internal", EI)

    ED = (0, 0, 440)
    drv = _box(325, ex1 - 8, -135, 10, z0, z0 + 45)
    drv = _fillet_try(drv, _par(drv, Axis.Z), [4.0, 2.0])
    for k in range(9):
        y = -128 + 14 * k
        drv -= _box(324, ex1 - 7, y, y + 6, z0 + 10, z0 + 46)
    add("Dual-channel motor driver (finned case)", drv, C_BLACK, "metal", 5, "internal", ED)

    ECn = (0, 0, 500)
    cons = []
    for y0 in (40.0, 88.0):
        c = _box(335, 400, y0, y0 + 42, z0, z0 + 58)
        c = _fillet_try(c, _par(c, Axis.Z), [6.0, 3.0])
        c += _zcyl(352, y0 + 21, z0 + 62, 5, 8) + _zcyl(383, y0 + 21, z0 + 62, 5, 8)
        cons.append(c)
    add("Main contactors (2)", _union(cons), C_CHAR, "plastic", 6, "internal", ECn)
    studs = _union([_hex_z(x, y0 + 21, z0 + 64, 9.0, 3.0) for y0 in (40.0, 88.0) for x in (352, 383)])
    add("Contactor studs", studs, C_COPPER, "metal", 6, "internal", ECn)
    knob = _ycyl(365, ey + 12, 270, 16, 24)
    knob = _fillet_try(knob, _ymax(knob), [4.0, 2.0])
    knob += _box(355, 375, ey + 20, ey + 30, 262, 278) + _box(363, 367, ey + 20, ey + 30, 252, 288)
    add("Battery disconnect knob", knob, C_RED, "plastic", 6, "shell", (0, 160, 200))
    dplate = _ycyl(365, ey + 1, 270, 24, 2)
    add("Disconnect backing plate", dplate, C_YELLOW, "plastic", 6, "shell", (0, 150, 200))

    ECt = (0, 0, 580)
    board = _box(325, ex1 - 8, -135, 10, z0 + 50, z0 + 52)
    add("Controller board", board, C_PCB, "plastic", 7, "internal", ECt)
    chips = _box(340, 380, -120, -80, z0 + 52, z0 + 56) + _box(345, 375, -115, -85, z0 + 56, z0 + 58) \
        + _box(400, 430, -60, -20, z0 + 52, z0 + 57) + _box(335, 440, -8, 4, z0 + 52, z0 + 62)
    add("Controller components", chips, C_CHIP, "plastic", 7, "internal", ECt)
    shield = _box(345, 375, -115, -85, z0 + 58, z0 + 59)
    add("Controller shield can", shield, C_METAL, "metal", 7, "internal", ECt)
    relay = _box(410, ex1 - 8, 40, 130, z0, z0 + 60)
    relay = _fillet_try(relay, _par(relay, Axis.Y), [3.0, 1.5])
    add("Dual-channel safety relay", relay, C_RELAY, "plastic", 7, "internal", ECt)
    rlab = _box(415, ex1 - 12, 55, 115, z0 + 60, z0 + 60.4)
    add("Safety relay label", rlab, C_LABEL, "paper", 7, "internal", ECt)
    rled = _zcyl(420, 50, z0 + 60.5, 2.2, 1.2)
    add("Safety relay status light (lit)", rled, "#22C55E", "emissive", 7, "internal", ECt)

    # ============================================================ 9 rear emergency stop
    EX = (160, 0, 200)
    bp = _box(ex1, ex1 + 3, -120, -40, 230, 305)
    bp = _fillet_try(bp, _par(bp, Axis.X), [6.0, 4.0])
    add("Emergency stop backing plate, rear", bp, C_YELLOW, "plastic", 9, "shell", EX)
    es = _xcyl(ex1 + 10, -80, 270, 14, 14) + _xcyl(ex1 + 22, -80, 270, 20, 12)
    es = _fillet_try(es, _xmax(es), [6.0, 4.0, 2.0])
    add("Emergency stop, rear", es, C_RED, "plastic", 9, "shell", EX)

    # ============================================================ 10 bumper hoop and safety edge
    bx = D["bumper_face_x"]
    bh = P["bumper_half_w"]
    b0, b1, ed = P["bumper_z0"], P["bumper_z1"], P["edge_depth"]
    x0b = P["bumper_x0"]
    EB = (320, 0, 0)
    outer = _box(x0b, bx, -bh, bh, b0, b1)
    outer = _fillet_try(outer, [e for e in _par(outer, Axis.Z) if e.center().X > bx - 1], [45.0, 30.0, 20.0])
    inner = _box(x0b - 1, bx - ed, -bh + 40, bh - 40, b0 - 1, b1 + 1)
    core = _box(x0b - 1, bx - 40, -bh + 15, bh - 15, b0 - 1, b1 + 1)
    core = _fillet_try(core, [e for e in _par(core, Axis.Z) if e.center().X > bx - 41], [30.0, 20.0])
    edge = outer - core
    edge = _fillet_try(edge, [e for e in edge.edges() if e.center().Z > b1 - 1 or e.center().Z < b0 + 1], [8.0, 5.0, 3.0])
    add("Contact bumper safety edge", edge, C_RUBBER, "rubber", 10, "shell", EB)
    hoop = (_box(x0b, bx - 40, -bh + 15, bh - 15, 72, 128) - _box(x0b - 1, bx - ed - 2, -bh + 40, bh - 40, 60, 140))
    hoop = _fillet_try(hoop, [e for e in _par(hoop, Axis.Z) if e.center().X > bx - 60], [22.0, 15.0])
    add("Bumper hoop, 40 x 20 mm tube", hoop, C_YELLOW, "painted", 10, "shell", EB)
    stripes = []
    for k in range(-5, 6):
        y = 40.0 * k
        stripes.append(_box(bx - 0.2, bx + 0.6, y - 9, y + 9, 88, 112))
    add("Safety edge marking", _union(stripes), C_YELLOW, "painted", 10, "shell", EB)
    mounts = []
    for s in (-1, 1):
        y0, y1 = (hy + 2 * t, bh - 40) if s > 0 else (-bh + 40, -hy - 2 * t)
        m = _box(P["cheek_x1"] - 20, bx - ed, y0, y1, 110, 130)
        mounts.append(_fillet_try(m, _par(m, Axis.Y), [4.0, 2.0]))
    add("Bumper mounts", _union(mounts), C_CHAR, "painted", 10, "shell", EB)

    # ============================================================ 11 UWB anchors on the bumper corners
    ay, at = P["anchor_y"], P["anchor_top"]
    EA = (440, 0, 80)
    for s, nm in ((-1, "left"), (1, "right")):
        rad = _box(bx - 40, bx - 5, s * ay - 18, s * ay + 18, b1, at)
        rad = _fillet_try(rad, _par(rad, Axis.Z), [8.0, 5.0])
        rad = _fillet_try(rad, _top(rad), [5.0, 3.0])
        add(f"UWB anchor radome, {nm}", rad, C_WHITE, "plastic", 11, "shell", EA)
        dot = _box(bx - 5, bx - 4.6, s * ay - 10, s * ay + 10, b1 + 22, b1 + 26)
        add(f"UWB anchor mark, {nm}", dot, C_ACCENT, "painted", 11, "shell", EA)

    # ============================================================ 13 manual release lever
    ER = (0, -220, 200)
    lev = _box(ex0 + 20, ex1 - 40, -ey - 30, -ey - 12, 252, 268)
    lev = _fillet_try(lev, _par(lev, Axis.X), [5.0, 3.0])
    lev += _box(ex1 - 60, ex1 - 40, -ey - 30, -ey, 240, 280)
    add("Manual release lever", lev, C_METAL, "metal", 13, "shell", ER)
    grip = _xcyl(ex0 + 45, -ey - 21, 260, 13, 50)
    grip = _fillet_try(grip, grip.edges(), [4.0, 2.0])
    add("Release lever grip", grip, C_RED, "rubber", 13, "shell", ER)

    # ============================================================ 18 obstacle lidar and bracket
    lx = D["lidar_x"]
    lz0 = P["lidar_scan_z"] - P["lidar_h"] / 2
    EL = (380, 0, 40)
    br = _box(P["plate_x1"] - 20, lx + 20, -35, 35, lz0 - 6, lz0) + _box(P["plate_x1"] - 20, P["plate_x1"], -35, 35, lz0 - 6, P["plate_z"])
    br = _fillet_try(br, _par(br, Axis.Y), [3.0, 1.5])
    add("Lidar bracket", br, C_CHAR, "painted", 18, "shell", EL)
    lr = P["lidar_d"] / 2
    base = _zcyl(lx, 0, lz0 + 8, lr, 16)
    base = _fillet_try(base, _bottom(base), [3.0, 1.5])
    add("Lidar base", base, C_BLACK, "plastic", 18, "shell", EL)
    band = _zcyl(lx, 0, lz0 + 24, lr - 1.5, 16)
    add("Lidar scan window", band, "#0B0E12", "screen", 18, "shell", EL)
    capl = _zcyl(lx, 0, lz0 + 36.5, lr - 1, 9)
    capl = _fillet_try(capl, _top(capl), [4.0, 2.0])
    add("Lidar top cap", capl, C_CHAR, "plastic", 18, "shell", EL)

    # ============================================================ 8 tiller head, 9, 11, 12 on it
    # Built in a local frame at the handle top (z along the handle, x toward the operator), then placed.
    Lt = Pos(tx, 0, tz) * Rot(0, HANDLE_DEG, 0)
    ET = (0, 0, 420)
    hub = Cylinder(24, 70).move(Location((0, 0, -25)))
    hub = _fillet_try(hub, _top(hub), [4.0, 2.0])
    body = _box(-45, 35, -44, 44, 5, 110)
    body = _fillet_try(body, _par(body, Axis.Z), [14.0, 10.0])
    body = _fillet_try(body, _top(body), [6.0, 4.0])
    tbody = hub + body
    tbody += _box(20, 58, -8, 8, 40, 84)                                   # spine to the grip bar
    tbody += Pos(58, 0, 70) * Rot(90, 0, 0) * Cylinder(13, 2 * GRIP_Y[0] + 4)
    add("Tiller control head body", Lt * tbody, C_CHAR, "plastic", 8, "accessory", ET)
    grips = []
    for s in (-1, 1):
        g = Pos(58, s * (GRIP_Y[0] + GRIP_Y[1]) / 2, 70) * Rot(90, 0, 0) * Cylinder(17, GRIP_Y[1] - GRIP_Y[0])
        g = _fillet_try(g, g.edges(), [3.0, 1.5])
        for k in range(1, 7):
            yk = s * (GRIP_Y[0] + k * (GRIP_Y[1] - GRIP_Y[0]) / 7)
            g -= Pos(58, yk, 70) * Rot(90, 0, 0) * (Cylinder(18, 2.0) - Cylinder(15.5, 3.0))
        grips.append(g)
    add("Tiller grips (rubber)", Lt * _union(grips), C_RUBBER, "rubber", 8, "accessory", ET)
    caps = _union([Pos(58, s * (GRIP_Y[1] + 3), 70) * Rot(90, 0, 0) * Cylinder(20, 6) for s in (-1, 1)])
    add("Tiller grip end caps", Lt * caps, C_ACCENT, "plastic", 8, "accessory", ET)
    wheels = []
    for s in (-1, 1):
        w_ = Pos(58, s * (GRIP_Y[0] - 5), 70) * Rot(90, 0, 0) * Cylinder(24, 7)
        for k in range(16):
            ang = 2 * math.pi * k / 16
            w_ -= Pos(58 + 24 * math.cos(ang), s * (GRIP_Y[0] - 5), 70 + 24 * math.sin(ang)) * Box(3, 9, 3)
        wheels.append(w_)
    add("Thumbwheel throttles", Lt * _union(wheels), C_METAL, "metal", 8, "accessory", ET)
    pad = _box(34, 62, -34, 34, 12, 46)
    pad = _fillet_try(pad, pad.edges(), [8.0, 5.0, 3.0])
    add("Belly-reverse paddle", Lt * pad, C_ACCENT, "rubber", 8, "accessory", ET)
    key = Pos(14, 24, 111) * Cylinder(10, 4)
    key -= Pos(14, 24, 113) * Box(2, 9, 3)
    add("Mode key switch (walk or follow)", Lt * key, C_METAL, "metal", 8, "accessory", ET)
    horn = Pos(14, -24, 112) * Cylinder(8, 6)
    horn = _fillet_try(horn, _top(horn), [2.0, 1.0])
    add("Horn button", Lt * horn, C_ACCENT, "plastic", 8, "accessory", ET)
    tlab = _box(-40, -18, -30, 30, 110, 110.4)
    add("Tiller head label", Lt * tlab, C_LABEL, "paper", 8, "accessory", ET)

    ebp = Pos(-20, -22, 111) * Cylinder(20, 3)
    add("Emergency stop backing, tiller", Lt * ebp, C_YELLOW, "plastic", 9, "accessory", ET)
    eh = Pos(-20, -22, 118) * Cylinder(10, 12) + Pos(-20, -22, 128) * Cylinder(16, 10)
    eh = _fillet_try(eh, _top(eh), [5.0, 3.0, 1.5])
    add("Emergency stop, tiller", Lt * eh, C_RED, "plastic", 9, "accessory", ET)

    bb_ = Pos(-20, 24, 116) * Cylinder(20, 12)
    bb_ = _fillet_try(bb_, _top(bb_), [2.0, 1.0])
    add("Status beacon base", Lt * bb_, C_BLACK, "plastic", 12, "accessory", ET)
    lens = Pos(-20, 24, 140) * Cylinder(16, 36) + Pos(-20, 24, 158) * Sphere(16)
    lens &= Pos(-20, 24, 150) * Box(40, 40, 50)
    add("Status beacon lens, amber (lit, walk mode)", Lt * lens, C_AMBER, "emissive", 12, "accessory", ET)

    anc = _box(-38, 0, -44 - 16, -44, 12, 60)
    anc = _fillet_try(anc, anc.edges(), [5.0, 3.0])
    add("UWB anchor radome, tiller", Lt * anc, C_WHITE, "plastic", 11, "accessory", ET)

    # ============================================================ 17 spiral-wrapped tiller cable
    s0 = 160.0
    p_h0 = piv + hdir * s0 + Vector(0, -26, 0)
    p_h1 = piv + hdir * (L - 60) + Vector(0, -26, 0)
    g0 = Vector(ex0 + 30, -26, etop)
    cable = _pipe([tuple(g0 + Vector(0, 0, 8)), tuple(g0 + Vector(0, 0, 60)), tuple(p_h0), tuple(p_h1),
                   tuple(piv + hdir * (L - 30) + Vector(0, -16, 0))], 5.0)
    rings = []
    nr = int((L - 60 - s0) / 28)
    for k in range(nr):
        c = piv + hdir * (s0 + 14 + 28 * k) + Vector(0, -26, 0)
        rings.append(Location(Plane(origin=c, z_dir=hdir)) * Torus(6.5, 1.8))
    clips = []
    for sk in (s0 + 40, L - 180):
        c = piv + hdir * sk
        clips.append(Location(Plane(origin=c + Vector(0, -13, 0), z_dir=hdir)) * Box(16, 30, 14))
    add("Tiller cable", cable, C_BLACK, "rubber", 17, "accessory", ET)
    add("Spiral wrap", _union(rings), "#3A3F47", "plastic", 17, "accessory", ET)
    add("Cable clips", _union(clips), C_CHAR, "plastic", 17, "accessory", ET)
    lg = _zcyl(ex0 + 30, -26, etop + 2.5, 10, 5) + _zcyl(ex0 + 30, -26, etop + 8, 7.5, 6)
    add("Lid cable gland", lg, C_BLACK, "plastic", 17, "shell", (0, 0, 830))

    # ============================================================ operator (context) and tag (15)
    gx = tx + 58 * math.cos(a) + 70 * math.sin(a)
    gz = tz - 58 * math.sin(a) + 70 * math.cos(a)
    hand_y = (GRIP_Y[0] + GRIP_Y[1]) / 2
    J = _pose_for(gz, hand_y)
    lm = mannequin_landmarks(PERSON_H, "push", **J)
    hl = lm["hands"][0]
    person = mannequin(PERSON_H, "push", **J)
    # figure faces -Y; turn it to face -X (toward the truck), hands onto the grip bar
    px, pz = gx - hl[1], gz - hl[2]
    place = Pos(px, 0, pz) * Rot(0, 0, -90)
    add("Operator, 1.75 m (walk mode)", place * person, C_CLAY, "clay", None, "context", (0, 0, 0))

    # belt and UWB tag on the figure's left hip (world -Y, toward the camera)
    pel = Vector(*lm["pelvis"])
    lean = math.radians(0.5 * lm["joints"]["torso_lean"])
    up_p = Vector(0, -math.sin(lean), math.cos(lean))
    c_pel = pel + Vector(0, -22, 0) * math.cos(lean) + up_p * 30
    bcen = c_pel + up_p * 62
    f_scale = math.sqrt(max(0.0, 1 - (62 / 130) ** 2))
    ra, rb = 168 * f_scale + 4, 118 * f_scale + 4
    pl = Plane(origin=bcen, x_dir=(1, 0, 0), z_dir=up_p)
    belt = extrude(pl * Ellipse(ra, rb), amount=36, both=False) - extrude(pl * Ellipse(ra - 5, rb - 5), amount=36)
    belt = Pos(*(up_p * -18)) * belt
    add("Operator belt", place * belt, C_FABRIC, "fabric", None, "context", (0, 0, 0))
    tag_c = bcen + Vector(ra + 12, 10, 0)
    tag = Pos(*tag_c) * Box(18, 56, 80)
    tag = _fillet_try(tag, tag.edges(), [7.0, 5.0, 3.0])
    ET2 = (-450, -300, -300)
    add("Operator UWB belt tag", place * tag, C_WHITE, "plastic", 15, "accessory", ET2)
    tband = Pos(*(tag_c + Vector(9.2, 0, 22))) * Box(0.6, 44, 6)
    add("Tag accent band", place * tband, C_ACCENT, "painted", 15, "accessory", ET2)
    tbtn = Pos(*(tag_c + Vector(10, 0, -12))) * Rot(0, 90, 0) * Cylinder(10, 5)
    tbtn = _fillet_try(tbtn, tbtn.edges(), [2.0, 1.0])
    add("Tag stop button", place * tbtn, C_RED, "rubber", 15, "accessory", ET2)
    tled = Pos(*(tag_c + Vector(9.4, 16, 22 - 12))) * Rot(0, 90, 0) * Cylinder(2.5, 1.0)
    add("Tag link light (lit)", place * tled, "#38BDF8", "emissive", 15, "accessory", ET2)
    return out


_POSE_CACHE = {}


def _pose_for(zt, lat):
    """Push-pose arm overrides that put both hands on a grip bar at height zt, `lat` mm either side."""
    key = (round(zt, 1), round(lat, 1))
    if key in _POSE_CACHE:
        return _POSE_CACHE[key]
    from context_parts import mannequin_landmarks
    j0 = mannequin_landmarks(PERSON_H, "push")["joints"]
    best = None
    v = [j0["shoulder_flex_l"], j0["elbow_flex_l"], -10.0]
    step = [4.0, 8.0, 4.0]
    def cost(q):
        sf, ef, ab = q
        h = mannequin_landmarks(PERSON_H, "push", shoulder_flex_l=sf, shoulder_flex_r=sf, elbow_flex_l=ef,
                                elbow_flex_r=ef, shoulder_abd_l=ab, shoulder_abd_r=ab)["hands"][0]
        return (h[0] - lat) ** 2 + (h[2] - zt) ** 2 + 0.2 * (h[1] + 470) ** 2
    best = cost(v)
    for _ in range(12):                          # coordinate search, then halve the steps
        improved = True
        while improved:
            improved = False
            for i in range(3):
                for sg in (-1, 1):
                    q = list(v); q[i] += sg * step[i]
                    c = cost(q)
                    if c < best:
                        best, v, improved = c, q, True
        step = [s / 2 for s in step]
    sf, ef, ab = v
    J = dict(shoulder_flex_l=sf, shoulder_flex_r=sf, elbow_flex_l=ef, elbow_flex_r=ef,
             shoulder_abd_l=ab, shoulder_abd_r=ab)
    _POSE_CACHE[key] = J
    return J


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.1f} cm3")
