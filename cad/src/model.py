"""PalletPilot parametric model (build123d), TRL 3, constructable design (PLP-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    constructability checks: overlaps, contacts, steering sweep

Every made part is drawn as it is cut, bent or welded, and every joint is a face-to-face
contact held by a named fixing (PLP-DDR-003 lists the changes from the concept model).
PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the truck, fork tips toward -X and the handle (drive) end toward +X;
Y across the forks (+Y is on the right for someone standing at the handle end facing the forks; the
release lever is on the left, -Y); Z up from the floor. Units mm.
The donor is a common 27 x 48 in (685 x 1220 mm) manual pallet jack. Donor parts are reference
geometry only and carry no BOM number. Every kit part hangs off the donor's steering yoke, so it
turns with the handle and never sits on the forks.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# ------------------------------------------------------------------ parameters (mm)
# Edit these, not the geometry below. docs/04-calcs/sizing.py imports this dict.
PARAMS = {
    # donor jack (reference; survey item under R1)
    "fork_len": 1160.0, "fork_w": 160.0, "fork_h": 55.0, "out_w": 685.0, "fork_top": 80.0,
    "x_tip": -1220.0, "load_roller_x": -1130.0,
    "kingpin_x": 110.0,        # steering axis X (steer wheel axle under it)
    "head_x1": 10.0,           # rear face of the jack's frame head (fixed, does not steer)
    "steer_r": 90.0, "steer_w": 50.0, "steer_y": 72.0,
    "yoke_z0": 204.0,          # underside of the steering yoke plate
    "yoke_top": 219.0,         # top of the steering yoke plate (the kit's top plate sits on it)
    "yoke_x1": 160.0,          # rear edge of the yoke plate
    "yoke_half_w": 110.0,
    "pump_r": 55.0,
    "pivot_z": 350.0, "handle_len": 900.0, "handle_r": 16.0, "handle_walk_deg": 20.0,
    # drive (BOM 1, 2)
    "drive_x": 290.0, "drive_r": 100.0, "drive_w": 60.0, "drive_track": 260.0,
    "plate_t": 6.0,            # top plate thickness
    "plate_x0": 125.0, "plate_x1": 420.0, "plate_half_w": 200.0,
    "plate_z": 219.0,          # underside of the top plate (= top of the yoke plate)
    "notch_r": 62.0,           # pump notch radius in the top plate
    "jaw_t": 10.0, "jaw_x1": 196.0, "jaw_half_w": 95.0,
    "clamp_bolt_x": 174.0, "clamp_bolt_y": (35.0, 80.0),
    "arm_y": 165.0, "arm_t": 10.0,                 # inner face of each drive arm, arm plate thickness
    "pivot_xz": (400.0, 145.0), "pivot_r": 10.0,   # rear pivot pin of the drive arms
    "cheek_x0": 205.0, "cheek_x1": 400.0,          # spring position and pivot position along X
    "spring_xz": (205.0, 50.0),                    # front end of each arm (spring tab)
    "spring_y": 192.0, "spring_r": 17.0, "spring_rate": 100.0,   # N/mm
    "tab_z": (45.0, 55.0),
    # release mechanism (BOM 13)
    "cam_xz": (200.0, 182.0), "shaft_r": 8.0, "cam_r": 36.0, "cam_e": 22.0, "axle_r": 10.0,
    "crank_len": 50.0, "lever_len": 400.0, "lever_pivot_xz": (415.0, 260.0),
    # enclosure (BOM 3), top under the handle sweep
    "enc_x0": 185.0, "enc_x1": 455.0, "enc_half_w": 150.0, "enc_z0": 225.0, "enc_top": 320.0,
    "enc_t": 2.0, "lid_t": 6.0,
    "pack_l": 270.0, "pack_w": 115.0, "pack_h": 85.0,
    # bumper (BOM 10): 40 x 20 x 2 tube hoop with a safety edge on the front and sides
    "bumper_clear": 30.0, "edge_depth": 70.0, "edge_travel": 40.0, "bumper_half_w": 240.0,
    "bumper_z0": 60.0, "bumper_z1": 140.0, "bumper_x0": 230.0,
    "hoop_z": (90.0, 130.0), "side_edge_t": 20.0,
    # UWB anchors (BOM 11) on the hoop's front corners, below the lidar scan plane
    "anchor_y": 225.0, "anchor_top": 180.0,
    # obstacle lidar (BOM 18)
    "lidar_d": 56.0, "lidar_h": 41.0, "lidar_scan_z": 200.0,
    # tiller head (BOM 8)
    "head_w": 220.0,
    # steering stops (BOM 19)
    "steer_stop_deg": 40.0, "stop_along": 130.0, "corner_clip": 50.0,
}


def derived(P=PARAMS):
    """Numbers the drawing and the calculation note use."""
    D = {}
    D["bumper_face_x"] = P["drive_x"] + P["drive_r"] + P["bumper_clear"] + P["edge_depth"]
    D["hoop_x0"] = D["bumper_face_x"] - P["edge_depth"]                # front tube rear face
    D["bare_rear_x"] = P["kingpin_x"] + P["steer_r"]
    D["added_length"] = D["bumper_face_x"] - D["bare_rear_x"]
    D["trail"] = P["drive_x"] - P["kingpin_x"]
    D["anchor_baseline"] = 2 * P["anchor_y"]
    a = math.radians(P["handle_walk_deg"])
    D["handle_top"] = (P["kingpin_x"] + P["handle_len"] * math.sin(a), P["pivot_z"] + P["handle_len"] * math.cos(a))
    D["handle_clear_90"] = (P["pivot_z"] - P["handle_r"]) - P["enc_top"]
    D["lidar_x"] = D["bumper_face_x"] - 10 - P["lidar_d"] / 2
    D["overall_len"] = D["bumper_face_x"] - P["x_tip"]
    D["bare_len"] = D["bare_rear_x"] - P["x_tip"]
    # drive arm lever ratio: spring tab and wheel axle, both measured from the rear pivot
    px = P["pivot_xz"][0]
    D["arm_ratio"] = (px - P["spring_xz"][0]) / (px - P["drive_x"])
    D["spring_force"] = 750.0 / D["arm_ratio"]                         # N per spring for 750 N per wheel
    D["spring_preload_mm"] = D["spring_force"] / P["spring_rate"]
    D["wheel_lift"] = (P["cam_e"] - D["spring_preload_mm"]) / D["arm_ratio"]
    D["cam_bottom"] = P["cam_xz"][1] - P["cam_e"] - P["cam_r"]          # cam underside, wheels down
    D["spring_len"] = D["cam_bottom"] - 8.0 - P["tab_z"][1]             # installed length under the saddle
    return D


# ------------------------------------------------------------------ geometry helpers
def box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def wheel(x, y, z, r, w):
    """Wheel with its axle along Y, centred on y."""
    from build123d import Cylinder, Pos, Rot
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def ycyl(x, z, r, y0, y1):
    """Cylinder along Y from y0 to y1."""
    return wheel(x, (y0 + y1) / 2, z, r, abs(y1 - y0))


def zcyl(x, y, r, z0, z1):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def capsule_y(a, b, r, y0, y1):
    """Flat bar with round ends in an X-Z plane between points a and b (x, z), from y0 to y1."""
    from build123d import Box, Pos, Rot
    (ax, az), (bx, bz) = a, b
    L = math.hypot(bx - ax, bz - az)
    ang = math.degrees(math.atan2(bz - az, bx - ax))
    t = abs(y1 - y0)
    yc = (y0 + y1) / 2
    bar = Pos((ax + bx) / 2, yc, (az + bz) / 2) * Rot(0, -ang, 0) * Box(L, t, 2 * r)
    return bar + ycyl(ax, az, r, y0, y1) + ycyl(bx, bz, r, y0, y1)


def mirror_y(shape):
    from build123d import Plane, mirror
    return mirror(shape, Plane.XZ)


Comp = namedtuple("Comp", "name shape color bom explode make")


# ------------------------------------------------------------------ components
def build_components(P=PARAMS):
    """Every component as built: {key: Comp}. Keys are used by the checks and the build plan pictures."""
    from build123d import Pos, Rot
    D = derived(P)
    C = {}

    def add(key, name, shape, color, bom=None, explode=(0, 0, 0), make="buy"):
        C[key] = Comp(name, shape, color, bom, explode, make)

    kx = P["kingpin_x"]
    # ---- donor manual jack (reference geometry; the head does not steer, the rest does)
    fy = P["out_w"] / 2 - P["fork_w"] / 2
    ft, fl, fw, fh, xt = P["fork_top"], P["fork_len"], P["fork_w"], P["fork_h"], P["x_tip"]
    forks = (box(xt, -60, fy - fw / 2, fy + fw / 2, ft - fh, ft) + box(xt, -60, -fy - fw / 2, -fy + fw / 2, ft - fh, ft))
    rollers = wheel(P["load_roller_x"], fy, 40, 40, 110) + wheel(P["load_roller_x"], -fy, 40, 40, 110)
    head = box(-60, P["head_x1"], -P["out_w"] / 2, P["out_w"] / 2, 25, 230)
    add("donor_fixed", "Donor jack frame and forks (not in kit)", forks + rollers + head, "#9CA3AF")
    yz0, yz1 = P["yoke_z0"], P["yoke_top"]
    yoke = box(kx - 50, P["yoke_x1"], -P["yoke_half_w"], P["yoke_half_w"], yz0, yz1)
    legs = box(kx - 30, kx + 30, 100, 108, 60, yz0) + box(kx - 30, kx + 30, -108, -100, 60, yz0)
    steer = (wheel(kx, P["steer_y"], P["steer_r"], P["steer_r"], P["steer_w"])
             + wheel(kx, -P["steer_y"], P["steer_r"], P["steer_r"], P["steer_w"]))
    pump = zcyl(kx, 0, P["pump_r"], yz1, P["pivot_z"])
    a = math.radians(P["handle_walk_deg"])
    L = P["handle_len"]
    shaft = (Pos(kx + L / 2 * math.sin(a), 0, P["pivot_z"] + L / 2 * math.cos(a))
             * Rot(0, P["handle_walk_deg"], 0) * zcyl(0, 0, P["handle_r"], -L / 2, L / 2))
    add("donor_yoke", "Donor yoke, pump, steer wheels and handle (not in kit)", yoke + legs + steer + pump + shaft, "#9CA3AF")
    tx, tz = D["handle_top"]

    # ---- 1 subframe: top plate with welded hangers, bumper brackets and lever bracket
    pz, pt = P["plate_z"], P["plate_t"]
    x0, x1, hw = P["plate_x0"], P["plate_x1"], P["plate_half_w"]
    top = box(x0, x1, -hw, hw, pz, pz + pt) - zcyl(kx, 0, P["notch_r"], pz - 1, pz + pt + 1)
    # clip the two front corners at 45 degrees so they stay inside the steering stop radius
    c = P["corner_clip"] / math.sqrt(2)
    for s in (1, -1):
        top -= Pos(x0, s * hw, pz + pt / 2) * Rot(0, 0, 45) * box(-c, c, -c, c, -pt, pt)
    for by in P["clamp_bolt_y"]:
        for s in (1, -1):
            top -= zcyl(P["clamp_bolt_x"], s * by, 6.5, pz - 1, pz + pt + 1)
    for (fx, fy_) in _feet_xy(P):
        top -= zcyl(fx, fy_, 4.5, pz - 1, pz + pt + 1)
    cx, cz = P["cam_xz"]
    fh_ = box(cx - 12, cx + 12, 174, 180, 160, pz) - ycyl(cx, cz, P["shaft_r"], 173, 181)       # front hanger, right
    px_, pz_ = P["pivot_xz"]
    rh = box(px_ - 14, px_ + 14, 180, 190, 125, pz) - ycyl(px_, pz_, P["pivot_r"], 179, 191)     # rear hanger, right
    bk = box(340, 380, 194, 200, 100, pz)                                                       # bumper bracket, right
    for bx_ in (350, 370):
        bk -= ycyl(bx_, 110, 4.5, 193, 201)
    right = fh_ + rh + bk
    lpx, lpz = P["lever_pivot_xz"]
    lb = (box(375, 435, -200, -194, pz + pt, 285) - ycyl(lpx, lpz, 6.0, -201, -193)
          + box(380, 395, -221, -200, 238, 250))                                                # lever bracket and stop
    add("subframe", "Subframe: top plate, hangers and brackets (welded)", top + right + mirror_y(right) + lb,
        "#374151", 1, (0, 0, 230), "make")

    # ---- 1 lower jaw with its packing bar (welded), and the four clamp bolts
    jt, jx1, jw = P["jaw_t"], P["jaw_x1"], P["jaw_half_w"]
    jaw = box(x0, jx1, -jw, jw, yz0 - jt, yz0) + box(P["yoke_x1"] + 2, jx1, -jw, jw, yz0, pz)
    bolts = None
    for by in P["clamp_bolt_y"]:
        for s in (1, -1):
            bx_, byy = P["clamp_bolt_x"], s * by
            jaw -= zcyl(bx_, byy, 6.5, yz0 - jt - 1, pz + 1)
            b_ = zcyl(bx_, byy, 9.5, yz0 - jt - 10, yz0 - jt) + zcyl(bx_, byy, 6.0, yz0 - jt, pz + pt) + zcyl(bx_, byy, 9.5, pz + pt, pz + pt + 10)
            bolts = b_ if bolts is None else bolts + b_
    add("jaw", "Lower jaw and packing bar", jaw, "#4B5563", 1, (0, 0, -140), "make")
    add("clamp_bolts", "Clamp bolts M12 (4), nuts on top", bolts, "#111827", 17, (0, 0, -140))

    # ---- 2 hub motors with axle spacers and nuts
    r, dx, dy = P["drive_r"], P["drive_x"], P["drive_track"] / 2
    ay0, at = P["arm_y"], P["arm_t"]
    m = None
    for s in (1, -1):
        w = wheel(dx, s * dy, r, r, P["drive_w"])
        y_out = dy + P["drive_w"] / 2
        stub = ycyl(dx, r, P["axle_r"], s * y_out, s * (ay0 + at + 8))
        spacer = ycyl(dx, r, 15.0, s * y_out, s * ay0)
        nut = ycyl(dx, r, 15.0, s * (ay0 + at), s * (ay0 + at + 8))
        m_ = w + stub + spacer + nut
        m = m_ if m is None else m + m_
    add("motors", "Hub motors (2), 200 mm, with brakes", m, "#111827", 2, (0, 0, -260))

    # ---- 1 drive arms (one each side), spring tab welded on
    def arm_shape():
        ax, az = P["spring_xz"]
        sh = capsule_y((px_, pz_), (dx, r), 18, ay0, ay0 + at) + capsule_y((dx, r), (ax, az), 18, ay0, ay0 + at)
        tz0, tz1 = P["tab_z"]
        sh += box(ax - 22, ax + 22, ay0, P["spring_y"] + P["spring_r"], tz0, tz1)
        sh -= ycyl(px_, pz_, P["pivot_r"], ay0 - 1, ay0 + at + 1)
        sh -= ycyl(dx, r, P["axle_r"], ay0 - 1, ay0 + at + 1)
        return sh
    arm = arm_shape()
    add("arm_r", "Drive arm, right", arm, "#0F766E", 1, (0, 140, 0), "make")
    add("arm_l", "Drive arm, left", mirror_y(arm), "#0F766E", 1, (0, -140, 0), "make")
    pin = ycyl(px_, pz_, P["pivot_r"], -196, 196)
    for s in (1, -1):
        pin += ycyl(px_, pz_, 15.0, s * (ay0 + at), s * 180) + ycyl(px_, pz_, 15.0, s * 190, s * 198)
    add("pivot_pin", "Arm pivot pin, spacers and nuts", pin, "#B45309", 1, (180, 0, 0), "make")

    # ---- 13 release mechanism: springs, saddles, straps, cam shaft, crank, link, lever
    sx, sy, sr = P["spring_xz"][0], P["spring_y"], P["spring_r"]
    tz1 = P["tab_z"][1]
    cb = D["cam_bottom"]
    springs = saddles = straps = None
    for s in (1, -1):
        sp = zcyl(sx, s * sy, sr, tz1, cb - 8) - zcyl(sx, s * sy, sr - 4, tz1 - 1, cb - 7)
        sd = box(sx - 22, sx + 22, s * (sy - sr), s * (sy + sr), cb - 8, cb)
        st = (box(sx - 26, sx - 22, s * (sy - 6), s * (sy + 6), P["tab_z"][0], cb)
              + box(sx + 22, sx + 26, s * (sy - 6), s * (sy + 6), P["tab_z"][0], cb))
        springs = sp if springs is None else springs + sp
        saddles = sd if saddles is None else saddles + sd
        straps = st if straps is None else straps + st
    add("springs", "Preload springs (2)", springs, "#D4A017", 13, (0, 0, 0))
    add("saddles", "Spring saddles (2)", saddles, "#A16207", 13, (0, 0, 60), "make")
    add("straps", "Lift straps (4)", straps, "#78716C", 13, (0, 0, 0), "make")
    sh_ = ycyl(cx, cz, P["shaft_r"], -221, 198)
    cams = None
    for s in (1, -1):
        cm = ycyl(cx, cz - P["cam_e"], P["cam_r"], s * 186, s * 198) - ycyl(cx, cz, P["shaft_r"], s * 185, s * 199)
        cams = cm if cams is None else cams + cm
    cl = P["crank_len"]
    # crank points up with the wheels down; lever and crank stay parallel through the link (a parallelogram)
    cp = (cx, cz + cl)
    crank = capsule_y((cx, cz), cp, 12, -221, -211) - ycyl(cx, cz, P["shaft_r"], -222, -210)
    add("camshaft", "Cam shaft, cams (2) and crank", sh_ + cams + crank + ycyl(cp[0], cp[1], 5.0, -229, -211),
        "#1D4ED8", 13, (0, 0, -120), "make")
    lp = (lpx, lpz + cl)
    link = capsule_y(cp, lp, 10, -229, -221)
    link -= ycyl(cp[0], cp[1], 5.0, -230, -220) + ycyl(lp[0], lp[1], 5.0, -230, -220)
    add("link", "Release link", link, "#6D28D9", 13, (0, -60, 0), "make")
    lever = box(lpx - P["lever_len"], lpx + 10, -221, -211, lpz - 10, lpz + 10) + capsule_y((lpx, lpz), lp, 10, -221, -211)
    lever -= ycyl(lpx, lpz, 6.0, -222, -210) + ycyl(lp[0], lp[1], 5.0, -222, -210)
    lever += ycyl(lpx - P["lever_len"] + 15, lpz, 14.0, -251, -221)                         # grip
    add("lever", "Release lever with grip", lever, "#DC2626", 13, (0, -80, 80), "make")
    add("lever_pins", "Lever pivot pin with spacer, and link pins",
        ycyl(lpx, lpz, 6.0, -221, -194) + ycyl(lpx, lpz, 10.0, -211, -200) + ycyl(lp[0], lp[1], 5.0, -229, -211),
        "#111827", 13, (0, -80, 80))

    # ---- 10 bumper: tube hoop, safety edge, bracket bolts
    hx0 = D["hoop_x0"]
    hz0, hz1 = P["hoop_z"]
    bf = D["bumper_face_x"]
    bh = P["bumper_half_w"]
    st_ = P["side_edge_t"]
    hy = bh - st_                    # outer face of the side tubes
    front = box(hx0, hx0 + 20, -hy, hy, hz0, hz1) - box(hx0 + 2, hx0 + 18, -hy + 2, hy - 2, hz0 + 2, hz1 - 2)
    side = box(P["bumper_x0"], hx0, hy - 20, hy, hz0, hz1) - box(P["bumper_x0"] - 1, hx0 + 1, hy - 18, hy - 2, hz0 + 2, hz1 - 2)
    side -= ycyl(350, 110, 5.5, hy - 21, hy - 17) + ycyl(370, 110, 5.5, hy - 21, hy - 17)
    hoop = front + side + mirror_y(side)
    add("hoop", "Bumper hoop, 40 x 20 x 2 tube", hoop, "#F59E0B", 10, (300, 0, 0), "make")
    edge = (box(hx0 + 20, bf, -bh, bh, P["bumper_z0"], P["bumper_z1"])
            + box(P["bumper_x0"], hx0 + 20, hy, bh, P["bumper_z0"] + 20, P["bumper_z1"])
            + box(P["bumper_x0"], hx0 + 20, -bh, -hy, P["bumper_z0"] + 20, P["bumper_z1"]))
    add("edge", "Safety edge (front and sides)", edge, "#111827", 10, (420, 0, 0))
    hb = None
    for s in (1, -1):
        for bx_ in (350, 370):
            b_ = (ycyl(bx_, 110, 7.0, s * 188, s * 194) + ycyl(bx_, 110, 4.0, s * 194, s * (hy - 20))
                  + ycyl(bx_, 110, 5.5, s * (hy - 20), s * (hy - 14)))          # M8 rivet nut in the tube wall
            hb = b_ if hb is None else hb + b_
    add("hoop_bolts", "Hoop bolts M8 (4) and rivet nuts", hb, "#111827", 17, (300, 0, 0))

    # ---- 11 UWB anchors on corner plates on the hoop, 18 lidar on a bent bracket
    ay, atop = P["anchor_y"], P["anchor_top"]
    anc = None
    for s in (1, -1):
        a_ = box(hx0, hx0 + 20, s * (hy - 15), s * hy, hz1, P["bumper_z1"]) + box(hx0 - 2, hx0 + 22, s * (ay - 18), s * (ay + 18), P["bumper_z1"], atop)
        anc = a_ if anc is None else anc + a_
    add("anchors", "UWB anchors (2) on corner plates", anc, "#7C3AED", 11, (300, 0, 120))
    lx = D["lidar_x"]
    lz0 = P["lidar_scan_z"] - P["lidar_h"] / 2
    lbr = (box(hx0, hx0 + 20, -20, 20, hz1, hz1 + 4) + box(hx0, hx0 + 4, -20, 20, hz1 + 4, lz0 - 6)
           + box(hx0, lx + 28, -25, 25, lz0 - 6, lz0))
    add("lidar_bracket", "Lidar bracket (bent strap)", lbr, "#64748B", 18, (300, 0, 200), "make")
    add("lidar", "Obstacle lidar", zcyl(lx, 0, P["lidar_d"] / 2, lz0, lz0 + P["lidar_h"]), "#0EA5E9", 18, (300, 0, 260))

    # ---- 3 enclosure with feet; 4 to 7 inside; 9 rear emergency stop
    ex0, ex1, ey, ez0, etop, et, lt = (P["enc_x0"], P["enc_x1"], P["enc_half_w"], P["enc_z0"], P["enc_top"],
                                       P["enc_t"], P["lid_t"])
    shell = box(ex0, ex1, -ey, ey, ez0, etop - lt) - box(ex0 + et, ex1 - et, -ey + et, ey - et, ez0 + et, etop)
    shell -= ycyl(365, 270, 20.0, ey - et - 1, ey + 1)                    # disconnect
    shell -= Pos(ex1 - et / 2, -80, 270) * Rot(0, 90, 0) * zcyl(0, 0, 11.0, -3, 3)   # rear emergency stop
    add("enclosure", "Enclosure, folded 2 mm aluminium", shell, "#0F766E", 3, (0, 0, 380), "make")
    feet = fb = None
    for (fx, fy_) in _feet_xy(P):
        s = 1 if fy_ > 0 else -1
        f_ = (box(fx - 12, fx + 12, s * ey, s * (ey + 20), ez0, ez0 + 3) + box(fx - 12, fx + 12, s * ey, s * (ey + 3), ez0 + 3, ez0 + 25))
        f_ -= zcyl(fx, fy_, 4.5, ez0 - 1, ez0 + 4)
        b_ = zcyl(fx, fy_, 7.0, ez0 + 3, ez0 + 9) + zcyl(fx, fy_, 4.0, pz, ez0 + 3) + zcyl(fx, fy_, 7.0, pz - 7, pz)
        feet = f_ if feet is None else feet + f_
        fb = b_ if fb is None else fb + b_
    add("feet", "Enclosure feet (4 angles, riveted)", feet, "#94A3B8", 3, (0, 0, 380), "make")
    add("feet_bolts", "Feet bolts M8 (4)", fb, "#111827", 17, (0, 0, 380))
    add("lid", "Enclosure lid", box(ex0, ex1, -ey, ey, etop - lt, etop), "#115E59", 3, (0, 0, 620), "make")
    z0 = ez0 + et
    pk0 = ex0 + 20
    add("pack", "LiFePO4 pack with BMS", box(pk0, pk0 + P["pack_w"], -P["pack_l"] / 2, P["pack_l"] / 2, z0, z0 + P["pack_h"]),
        "#D4A017", 4, (0, 0, 470))
    add("driver", "Motor driver", box(325, ex1 - 8, -135, 10, z0, z0 + 45), "#B45309", 5, (0, 0, 470))
    add("contactor", "Contactors (2), fuse and disconnect",
        box(335, 400, 40, 82, z0, z0 + 65) + box(335, 400, 88, 130, z0, z0 + 65) + ycyl(365, 270, 20.0, ey - et, ey + 25),
        "#991B1B", 6, (0, 0, 470))
    add("controller", "Controller and safety relay",
        box(325, ex1 - 8, -135, 10, z0 + 50, z0 + 65) + box(410, ex1 - 8, 40, 130, z0, z0 + 60), "#15803D", 7, (0, 0, 470))
    add("estop", "Emergency stop, enclosure rear", Pos(ex1 + 14, -80, 270) * Rot(0, 90, 0) * zcyl(0, 0, 20.0, -14, 14)
        + Pos(ex1 - et / 2, -80, 270) * Rot(0, 90, 0) * zcyl(0, 0, 11.0, -et / 2, et / 2), "#DC2626", 9, (120, 0, 0))

    # ---- 8 tiller head (socket over the handle tube), 12 beacon, 9 head stop, 11 head anchor
    hw_ = P["head_w"]
    head_ = (Pos(tx + 20, 0, tz - 30) * box(-45, 45, -hw_ / 2, hw_ / 2, -55, 55)
             + box(tx + 60, tx + 90, -60, 60, tz - 90, tz - 20)) - shaft
    add("tiller", "Tiller control head", head_, "#1F2937", 8, (0, 0, 160))
    add("beacon", "Status beacon and buzzer", zcyl(tx + 20, 70, 22, tz + 25, tz + 85), "#38BDF8", 12, (0, 0, 220))
    add("estop_head", "Emergency stop, tiller", zcyl(tx + 10, -40, 20, tz + 25, tz + 47), "#DC2626", 9, (0, 0, 220))
    add("anchor_head", "UWB anchor, tiller", box(tx - 5, tx + 35, -hw_ / 2 - 35, -hw_ / 2, tz - 40, tz), "#7C3AED", 11, (0, -80, 160))

    # ---- 19 steering stops: rubber blocks on the top plate's front corners
    stops = None
    for s in (1, -1):
        st_b = _steer_stop(P, s)
        stops = st_b if stops is None else stops + st_b
    add("steer_stops", "Steering stops (2), rubber", stops, "#111827", 19, (-120, 0, 0), "make")
    return C


def _feet_xy(P=PARAMS):
    y = P["enc_half_w"] + 12
    return [(205.0, y), (205.0, -y), (395.0, y), (395.0, -y)]


def _steer_stop(P, s):
    """A rubber block under the top plate's clipped front corner. When the yoke has turned by the stop
    angle, its outer face lies flat on the rear face of the jack's frame head. s = +1 or -1 (turning
    direction; the block sits on the +Y or -Y corner)."""
    from build123d import Pos, Rot
    kx = P["kingpin_x"]
    d = kx - P["head_x1"]                         # steering axis to the head face
    th = math.radians(P["steer_stop_deg"])
    n = (math.cos(th), -s * math.sin(th))         # the head face, seen from the turned kit, is n.q = -d
    t = (math.sin(th), s * math.cos(th))
    along, half_t = P["stop_along"], 20.0
    qx = -d * n[0] + half_t * n[0] + along * t[0]
    qy = -d * n[1] + half_t * n[1] + along * t[1]
    ang = math.degrees(math.atan2(n[1], n[0]))
    pz = P["plate_z"]
    return Pos(kx + qx, qy, pz - 10) * Rot(0, 0, ang) * box(-half_t, half_t, -20, 20, -10, 10)


# ------------------------------------------------------------------ compatibility with concept_media and sizing
BOM_GROUPS = {
    1: ("Drive module: subframe, jaw, arms and pivot", ["subframe", "jaw", "arm_r", "arm_l", "pivot_pin"], "#374151", (0, 0, 160)),
    2: ("Hub motors, 24 V, 200 mm, with brakes", ["motors"], "#111827", (0, -420, 0)),
    3: ("Battery and electronics enclosure", ["enclosure", "feet"], "#0F766E", (620, 0, 260)),
    4: ("LiFePO4 pack 25.6 V 20 Ah with BMS", ["pack"], "#D4A017", (620, 0, 460)),
    5: ("Dual-channel motor driver", ["driver"], "#B45309", (760, 0, 580)),
    6: ("Contactors (2), fuse and disconnect", ["contactor"], "#991B1B", (760, 0, 720)),
    7: ("Controller and safety relay", ["controller"], "#15803D", (760, 0, 860)),
    8: ("Tiller control head", ["tiller"], "#1F2937", (260, 0, 120)),
    9: ("Emergency stops (2)", ["estop", "estop_head"], "#DC2626", (720, 0, 260)),
    10: ("Contact bumper (hoop and safety edge)", ["hoop", "edge"], "#F59E0B", (420, 0, 0)),
    11: ("UWB anchors (3)", ["anchors", "anchor_head"], "#7C3AED", (560, 0, 0)),
    12: ("Status beacon and buzzer", ["beacon"], "#38BDF8", (260, 0, 260)),
    13: ("Manual release: cam shaft, lever, springs", ["springs", "saddles", "straps", "camshaft", "link", "lever", "lever_pins"], "#E5E7EB", (620, -260, 260)),
    18: ("Obstacle lidar and bracket", ["lidar", "lidar_bracket"], "#0EA5E9", (700, 0, 60)),
    19: ("Steering stops", ["steer_stops"], "#111827", (-200, 0, 0)),
}


def build_parts(P=PARAMS, comps=None):
    """Return {key: (name, shape, color, bom, explode offset)}: the donor plus one entry per BOM line.
    Used by concept_media.py, sheets.py and the calculation note."""
    from build123d import Compound
    C = comps or build_components(P)
    out = {"donor": ("Donor manual pallet jack (not in kit)",
                     Compound(children=[C["donor_fixed"].shape, C["donor_yoke"].shape]), "#9CA3AF", None, (0, 0, 0))}
    lid = C["lid"]
    for bom, (name, keys, color, exp) in BOM_GROUPS.items():
        out[f"bom{bom}"] = (name, Compound(children=[C[k].shape for k in keys]), color, bom, exp)
    out["lid"] = ("Enclosure lid", lid.shape, "#115E59", None, (620, 0, 980))
    fix = [k for k, c in C.items() if c.bom == 17]
    out["fixings"] = ("Bolts and nuts", Compound(children=[C[k].shape for k in fix]), "#111827", None, (0, 0, 0))
    return out


def kit_keys(parts):
    return [k for k in parts if k != "donor"]


def build(P=PARAMS, with_donor=True):
    from build123d import Compound
    parts = build_parts(P)
    keys = list(parts) if with_donor else kit_keys(parts)
    return Compound(children=[parts[k][1] for k in keys])


# ------------------------------------------------------------------ constructability checks
CONTACTS = [
    ("subframe", "donor_yoke"), ("jaw", "donor_yoke"), ("jaw", "subframe"), ("clamp_bolts", "jaw"), ("clamp_bolts", "subframe"),
    ("arm_r", "pivot_pin"), ("arm_l", "pivot_pin"), ("pivot_pin", "subframe"), ("motors", "arm_r"), ("motors", "arm_l"),
    ("springs", "arm_r"), ("springs", "arm_l"), ("springs", "saddles"), ("saddles", "camshaft"), ("straps", "saddles"),
    ("straps", "arm_r"), ("straps", "arm_l"), ("camshaft", "subframe"), ("camshaft", "link"), ("link", "lever"),
    ("lever", "subframe"), ("lever_pins", "lever"), ("lever_pins", "subframe"), ("lever_pins", "link"),
    ("hoop", "subframe"), ("hoop_bolts", "hoop"), ("hoop_bolts", "subframe"), ("edge", "hoop"),
    ("anchors", "hoop"), ("lidar_bracket", "hoop"), ("lidar", "lidar_bracket"),
    ("feet", "enclosure"), ("feet", "subframe"), ("feet_bolts", "feet"), ("feet_bolts", "subframe"), ("lid", "enclosure"),
    ("pack", "enclosure"), ("driver", "enclosure"), ("contactor", "enclosure"), ("controller", "enclosure"),
    ("estop", "enclosure"), ("tiller", "donor_yoke"), ("beacon", "tiller"), ("estop_head", "tiller"), ("anchor_head", "tiller"),
    ("steer_stops", "subframe"),
]
# shapes that overlap on purpose: none in the kit. Donor parts are reference; the two donor groups are not checked
# against each other.
ALLOWED = {frozenset(("donor_fixed", "donor_yoke"))}


def _solids(shape):
    return list(shape.solids()) or [shape]


def _bb_apart(A, B, pad=0.0):
    return (A.min.X > B.max.X + pad or B.min.X > A.max.X + pad or A.min.Y > B.max.Y + pad or B.min.Y > A.max.Y + pad
            or A.min.Z > B.max.Z + pad or B.min.Z > A.max.Z + pad)


def check_fits(C=None, tol=1.0, verbose=True):
    """No two components may share volume (more than tol mm3), and every CONTACTS pair must touch."""
    C = C or build_components()
    keys = list(C)
    sol = {k: [(s, s.bounding_box()) for s in _solids(C[k].shape)] for k in keys}
    bbs = {k: C[k].shape.bounding_box() for k in keys}
    overlaps = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if frozenset((a, b)) in ALLOWED or _bb_apart(bbs[a], bbs[b]):
                continue
            v = 0.0
            for sa, ba in sol[a]:
                for sb, bb_ in sol[b]:
                    if _bb_apart(ba, bb_):
                        continue
                    r = sa & sb
                    try:
                        v += r.volume if r is not None else 0.0
                    except Exception:
                        pass
            if v >= tol:
                overlaps.append((a, b, v))
    gaps = []
    for a, b in CONTACTS:
        pairs = [(sa, sb) for sa, ba in sol[a] for sb, bb_ in sol[b] if not _bb_apart(ba, bb_, 1.0)]
        d = min((sa.distance_to(sb) for sa, sb in pairs), default=99.0)
        if d > 0.05:
            gaps.append((a, b, d))
    if verbose:
        print(f"fit check: {len(keys)} components, {len(overlaps)} overlaps, {len(gaps)} missing contacts "
              f"({len(CONTACTS)} contacts checked)")
        for o in overlaps:
            print(f"  OVERLAP {o[0]} / {o[1]}: {o[2]:.1f} mm3")
        for g in gaps:
            print(f"  NO CONTACT {g[0]} / {g[1]}: {g[2]:.2f} mm apart")
    return overlaps, gaps


STEERS = None   # every key except the fixed donor frame turns with the yoke


def steer_clear(C=None, deg=None, verbose=True):
    """Turn everything on the yoke about the steering axis and look for contact with the fixed frame.
    Returns the largest angle (both ways, 1 degree steps) at which nothing on the yoke, apart from the steering
    stops, touches the frame, and the angle at which the stops meet the frame."""
    from build123d import Pos, Rot
    C = C or build_components()
    P = PARAMS
    kx = P["kingpin_x"]
    fixed = C["donor_fixed"].shape
    fsol = _solids(fixed)
    head = [s for s in fsol if s.bounding_box().max.X > P["head_x1"] - 1]
    moving = [k for k in C if k not in ("donor_fixed", "donor_yoke", "steer_stops") and C[k].bom is not None]
    res = {}
    for s in (1, -1):
        first_hit, stop_hit = None, None
        for a in range(5, 91):
            T = Pos(kx, 0, 0) * Rot(0, 0, s * a) * Pos(-kx, 0, 0)
            if stop_hit is None:
                st = T * C["steer_stops"].shape
                if min(st.distance_to(h) for h in head) < 0.5:
                    stop_hit = a
            if first_hit is None:
                for k in moving:
                    sh = T * C[k].shape
                    bb = sh.bounding_box()
                    if bb.min.X > P["head_x1"] + 0.5:
                        continue
                    if any(not _bb_apart(bb, h.bounding_box()) and (sh & h).volume > 0.5 for h in head):
                        first_hit = (a, k)
                        break
            if first_hit and stop_hit:
                break
        res[s] = (stop_hit, first_hit)
        if verbose:
            print(f"steering {'right' if s > 0 else 'left'}: stops meet the frame at {stop_hit} deg; "
                  f"first kit part to reach the frame: {first_hit}")
    return res


def release_state(C=None, P=PARAMS):
    """The moving parts with the release lever raised (wheels lifted for pushing by hand)."""
    from build123d import Pos, Rot
    C = C or build_components(P)
    D = derived(P)
    cx, cz = P["cam_xz"]
    lpx, lpz = P["lever_pivot_xz"]
    cl = P["crank_len"]
    rot = lambda sh, x, z, a: Pos(x, 0, z) * Rot(0, a, 0) * Pos(-x, 0, -z) * sh   # noqa: E731
    px_, pz_ = P["pivot_xz"]
    tab_rise = P["cam_e"] - D["spring_preload_mm"]
    arm_deg = math.degrees(tab_rise / (px_ - P["spring_xz"][0]))
    return {
        "camshaft": rot(C["camshaft"].shape, cx, cz, 90),
        "lever": rot(C["lever"].shape, lpx, lpz, 90),
        "lever_pins": rot(C["lever_pins"].shape, lpx, lpz, 90),
        "link": Pos(cl, 0, -cl) * C["link"].shape,
        "saddles": Pos(0, 0, P["cam_e"]) * C["saddles"].shape,
        "arm_r": rot(C["arm_r"].shape, px_, pz_, arm_deg),
        "arm_l": rot(C["arm_l"].shape, px_, pz_, arm_deg),
        "motors": rot(C["motors"].shape, px_, pz_, arm_deg),
    }


def check_release(C=None, tol=1.0, verbose=True):
    """No moving part may run into a fixed part, or into another moving part, with the lever raised.
    The lever pins, link pins and cam shaft turn in the parts they pass through, so those pairs are left out."""
    C = C or build_components()
    R = release_state(C)
    joined = {frozenset(p) for p in (("lever", "lever_pins"), ("link", "lever_pins"), ("camshaft", "link"),
                                     ("arm_r", "motors"), ("arm_l", "motors"))}
    skip = {"springs", "straps", "donor_fixed"}
    hits = []
    keys = [k for k in C if k not in skip]
    for a in R:
        for b in keys:
            if a == b or frozenset((a, b)) in joined:
                continue
            sb = R.get(b, C[b].shape)
            if b in R and keys.index(b) < keys.index(a):
                continue
            if _bb_apart(R[a].bounding_box(), sb.bounding_box()):
                continue
            v = 0.0
            for x in _solids(R[a]):
                for y in _solids(sb):
                    if not _bb_apart(x.bounding_box(), y.bounding_box()):
                        r_ = x & y
                        v += r_.volume if r_ is not None else 0.0
            if v >= tol:
                hits.append((a, b, v))
    if verbose:
        print(f"release state: {len(hits)} collisions")
        for h in hits:
            print(f"  COLLISION {h[0]} / {h[1]}: {h[2]:.1f} mm3")
    lifted = R["motors"].bounding_box().min.Z
    if verbose:
        print(f"release state: drive wheels {lifted:.1f} mm clear of the floor")
    return hits, lifted


def masses(C=None):
    """Mass of each made steel and aluminium part from its modelled volume (kg)."""
    C = C or build_components()
    rho = {"steel": 7.85e-6, "alu": 2.70e-6, "rubber": 1.3e-6}
    mat = {"subframe": "steel", "jaw": "steel", "arm_r": "steel", "arm_l": "steel", "pivot_pin": "steel",
           "saddles": "steel", "straps": "steel", "camshaft": "steel", "link": "steel", "lever": "steel",
           "hoop": "steel", "lidar_bracket": "steel", "enclosure": "alu", "lid": "alu", "feet": "alu",
           "steer_stops": "rubber", "clamp_bolts": "steel", "hoop_bolts": "steel", "feet_bolts": "steel",
           "lever_pins": "steel"}
    return {k: C[k].shape.volume * rho[m] for k, m in mat.items()}


if __name__ == "__main__":
    if "--check" in sys.argv:
        C = build_components()
        ov, gp = check_fits(C)
        sc = steer_clear(C)
        rh, lifted = check_release(C)
        ok_steer = all(st is not None and (fh is None or fh[0] > st) for st, fh in sc.values())
        D = derived()
        print(f"arm ratio {D['arm_ratio']:.3f}; spring force {D['spring_force']:.0f} N each; preload compression "
              f"{D['spring_preload_mm']:.1f} mm; wheel lift with the lever up {D['wheel_lift']:.1f} mm; "
              f"spring installed length {D['spring_len']:.1f} mm")
        for k, v in masses(C).items():
            print(f"  mass {k}: {v:.2f} kg")
        ok = not (ov or gp or rh) and ok_steer and lifted > 5
        print("constructability checks:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    parts = build_parts(comps=C)
    groups = {
        "palletpilot-assembly": [p[1] for p in parts.values()],
        "palletpilot-kit": [parts[k][1] for k in kit_keys(parts)],
        "drive-module": [C[k].shape for k in ("subframe", "jaw", "clamp_bolts", "arm_r", "arm_l", "pivot_pin", "motors",
                                              "springs", "saddles", "straps", "camshaft", "link", "lever", "lever_pins", "steer_stops")],
        "enclosure": [C[k].shape for k in ("enclosure", "feet", "feet_bolts", "lid", "pack", "driver", "contactor", "controller", "estop")],
        "bumper-and-sensors": [C[k].shape for k in ("hoop", "edge", "hoop_bolts", "anchors", "lidar", "lidar_bracket")],
        "tiller-head": [C[k].shape for k in ("tiller", "beacon", "estop_head", "anchor_head")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
    D = derived()
    print("exported STEP and STL to cad/step and cad/stl:", ", ".join(groups))
    print(f"bumper face X {D['bumper_face_x']:.0f} mm; added length {D['added_length']:.0f} mm; "
          f"handle clearance at 90 deg {D['handle_clear_90']:.0f} mm; anchor baseline {D['anchor_baseline']:.0f} mm")
