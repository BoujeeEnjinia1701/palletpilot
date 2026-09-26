"""PalletPilot parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

Level of detail: massing plus. Interfaces and main dimensions are right (yoke clamp,
drive axle, wheel envelope, enclosure envelope under the handle sweep, bumper line,
lidar scan plane, anchor baseline); fabrication detail is not modelled.
PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the truck, fork tips toward -X and the handle (drive) end toward +X;
Y across the forks; Z up from the floor. Units mm. The donor is a common 27 x 48 in
(685 x 1220 mm) manual pallet jack with a 75 to 80 mm lowered fork height. Donor
parts are reference geometry only and carry no BOM number. Every kit part hangs off
the donor's steering yoke, so it turns with the handle and never sits on the forks.
"""
import math
from pathlib import Path

# ------------------------------------------------------------------ parameters (mm)
# Edit these, not the geometry below. docs/04-calcs/sizing.py imports this dict.
PARAMS = {
    # donor jack (reference; survey item under R1)
    "fork_len": 1160.0,        # fork channel length
    "fork_w": 160.0,           # fork channel width
    "fork_h": 55.0,            # fork channel depth
    "out_w": 685.0,            # outside width over forks (27 in)
    "fork_top": 80.0,          # lowered fork top height (about 3 in)
    "x_tip": -1220.0,          # fork tips (48 in forks)
    "load_roller_x": -1130.0,  # load roller axle X
    "kingpin_x": 110.0,        # steering axis X (steer wheel axle under it)
    "steer_r": 90.0,           # steer wheel radius (180 mm wheels)
    "steer_w": 50.0,
    "steer_y": 72.0,           # steer wheel center offset from the axis
    "yoke_top": 175.0,         # top of the steering yoke plate
    "pivot_z": 350.0,          # handle pivot height on the pump
    "handle_len": 900.0,
    "handle_r": 16.0,
    "handle_walk_deg": 20.0,   # handle angle from vertical shown in the model
    # drive module (BOM 1, 2)
    "drive_x": 290.0,          # drive axle X
    "drive_r": 100.0,          # 200 mm (8 in) hub motor wheel
    "drive_w": 60.0,
    "drive_track": 260.0,      # center-to-center of the two drive wheels
    "plate_t": 6.0,            # subframe steel plate thickness
    "plate_x0": 170.0,
    "plate_x1": 420.0,
    "plate_z": 205.0,          # underside of the subframe top plate
    "plate_half_w": 180.0,
    "cheek_x0": 230.0,
    "cheek_x1": 350.0,
    # enclosure (BOM 3), sized to sit under the handle when the handle is horizontal
    "enc_x0": 185.0,
    "enc_x1": 455.0,
    "enc_half_w": 150.0,
    "enc_z0": 225.0,
    "enc_top": 320.0,          # including the lid; handle bottom at 90 deg is pivot_z - handle_r
    "enc_t": 1.5,
    # battery pack (BOM 4): 8S6P 26650 LiFePO4 in three layers
    "pack_l": 270.0, "pack_w": 115.0, "pack_h": 85.0,
    # bumper (BOM 10)
    "bumper_clear": 30.0,      # rigid hoop inner face to the drive wheel tread
    "edge_depth": 70.0,        # hoop plus safety edge profile, front to back
    "edge_travel": 40.0,       # safety edge compression travel before bottoming
    "bumper_half_w": 240.0,
    "bumper_z0": 50.0, "bumper_z1": 150.0,
    "bumper_x0": 180.0,        # rear end of the U hoop side arms
    # UWB anchors (BOM 11): on the bumper corners, below the lidar scan plane
    "anchor_y": 225.0,         # baseline = 2 x anchor_y = 450 mm
    "anchor_top": 185.0,
    # obstacle lidar (BOM 18): 2D lidar, puck 56 mm diameter
    "lidar_d": 56.0, "lidar_h": 41.0,
    "lidar_scan_z": 200.0,
    # tiller head (BOM 8)
    "head_w": 220.0,
}


def derived(P=PARAMS):
    """Numbers the drawing and the calculation note use."""
    D = {}
    D["bumper_face_x"] = P["drive_x"] + P["drive_r"] + P["bumper_clear"] + P["edge_depth"]
    D["bare_rear_x"] = P["kingpin_x"] + P["steer_r"]            # rear of the steer wheels at floor level
    D["added_length"] = D["bumper_face_x"] - D["bare_rear_x"]
    D["trail"] = P["drive_x"] - P["kingpin_x"]                  # drive axle ahead of the steering axis
    D["anchor_baseline"] = 2 * P["anchor_y"]
    a = math.radians(P["handle_walk_deg"])
    D["handle_top"] = (P["kingpin_x"] + P["handle_len"] * math.sin(a), P["pivot_z"] + P["handle_len"] * math.cos(a))
    # handle clearance over the enclosure with the handle horizontal (worst case)
    D["handle_clear_90"] = (P["pivot_z"] - P["handle_r"]) - P["enc_top"]
    # lidar center X: just inside the bumper face so the bumper takes contact first
    D["lidar_x"] = D["bumper_face_x"] - 10 - P["lidar_d"] / 2
    D["overall_len"] = D["bumper_face_x"] - P["x_tip"]
    D["bare_len"] = D["bare_rear_x"] - P["x_tip"]
    return D


# ------------------------------------------------------------------ geometry helpers
def box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def wheel(x, y, z, r, w):
    """Wheel with its axle along Y."""
    from build123d import Cylinder, Pos, Rot
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def build_parts(P=PARAMS):
    """Return {key: (name, shape, color, bom, explode offset)} for the donor and every kit part."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(P)
    out = {}

    # donor manual jack (reference)
    fy = P["out_w"] / 2 - P["fork_w"] / 2
    ft, fl, fw, fh, xt = P["fork_top"], P["fork_len"], P["fork_w"], P["fork_h"], P["x_tip"]
    forks = (box(xt, xt + fl, fy - fw / 2, fy + fw / 2, ft - fh, ft)
             + box(xt, xt + fl, -fy - fw / 2, -fy + fw / 2, ft - fh, ft))
    rollers = wheel(P["load_roller_x"], fy, 40, 40, 110) + wheel(P["load_roller_x"], -fy, 40, 40, 110)
    head = box(-60, 40, -P["out_w"] / 2, P["out_w"] / 2, 25, 230)
    kx = P["kingpin_x"]
    pump = Pos(kx, 0, 250) * Cylinder(55, 200)
    yoke = box(kx - 50, kx + 50, -110, 110, 150, P["yoke_top"])
    steer = (wheel(kx, P["steer_y"], P["steer_r"], P["steer_r"], P["steer_w"])
             + wheel(kx, -P["steer_y"], P["steer_r"], P["steer_r"], P["steer_w"]))
    a = math.radians(P["handle_walk_deg"])
    L = P["handle_len"]
    shaft = (Pos(kx + L / 2 * math.sin(a), 0, P["pivot_z"] + L / 2 * math.cos(a))
             * Rot(0, P["handle_walk_deg"], 0) * Cylinder(P["handle_r"], L))
    tx, tz = D["handle_top"]
    out["donor"] = ("Donor manual pallet jack (not in kit)",
                    forks + rollers + head + pump + yoke + steer + shaft, "#9CA3AF", None, (0, 0, 0))

    # 1 drive module subframe: yoke clamp, top plate, two trailing cheeks, spring towers
    t = P["plate_t"]
    hy = P["drive_track"] / 2 + P["drive_w"] / 2 + 5
    sub = (box(P["plate_x0"], P["plate_x1"], -P["plate_half_w"], P["plate_half_w"], P["plate_z"], P["plate_z"] + 20)
           + box(P["plate_x0"], P["plate_x0"] + 20, -40, 40, 140, P["plate_z"])                   # yoke clamp
           + box(kx + 10, P["plate_x0"], -40, 40, 140, 150)                                       # clamp tongue under the yoke
           + box(P["cheek_x0"], P["cheek_x1"], hy, hy + t * 2, 70, P["plate_z"])
           + box(P["cheek_x0"], P["cheek_x1"], -hy - t * 2, -hy, 70, P["plate_z"]))
    sub = sub + Pos(P["drive_x"] - 70, hy + 30, 185) * Cylinder(18, 40) + Pos(P["drive_x"] - 70, -hy - 30, 185) * Cylinder(18, 40)
    out["subframe"] = ("Drive module subframe and preload springs", sub, "#374151", 1, (0, 0, 160))

    # 2 hub motors
    r, dx, dy = P["drive_r"], P["drive_x"], P["drive_track"] / 2
    out["motors"] = ("Hub motors, 24 V, 200 mm, with brakes",
                     wheel(dx, dy, r, r, P["drive_w"]) + wheel(dx, -dy, r, r, P["drive_w"]), "#111827", 2, (0, -420, 0))

    # 3 enclosure shell and lid, all below the handle sweep
    ex0, ex1, ey, ez0, etop, et = P["enc_x0"], P["enc_x1"], P["enc_half_w"], P["enc_z0"], P["enc_top"], P["enc_t"] * 2
    lid_t = 6.0
    shell = box(ex0, ex1, -ey, ey, ez0, etop - lid_t) - box(ex0 + et, ex1 - et, -ey + et, ey - et, ez0 + et, etop)
    out["enclosure"] = ("Battery and electronics enclosure", shell, "#0F766E", 3, (620, 0, 260))
    out["lid"] = ("Enclosure lid", box(ex0, ex1, -ey, ey, etop - lid_t, etop), "#115E59", None, (620, 0, 980))

    # 4 pack, 5 driver, 6 contactors, 7 controller (inside the enclosure)
    z0 = ez0 + et
    out["pack"] = ("LiFePO4 pack 25.6 V 20 Ah with BMS",
                   box(ex0 + 8, ex0 + 8 + P["pack_w"], -P["pack_l"] / 2, P["pack_l"] / 2, z0, z0 + P["pack_h"]),
                   "#D4A017", 4, (620, 0, 460))
    out["driver"] = ("Dual-channel motor driver", box(325, ex1 - 8, -135, 10, z0, z0 + 45), "#B45309", 5, (760, 0, 580))
    # two main contactors in series, one per safety relay channel (PLP-DDR-002, O6)
    out["contactor"] = ("Contactors (2), fuse and disconnect",
                        box(335, 400, 40, 82, z0, z0 + 65) + box(335, 400, 88, 130, z0, z0 + 65)
                        + Pos(365, ey + 15, 270) * Rot(90, 0, 0) * Cylinder(20, 30), "#991B1B", 6, (760, 0, 720))
    out["controller"] = ("Controller and safety relay",
                         box(325, ex1 - 8, -135, 10, z0 + 50, z0 + 65) + box(410, ex1 - 8, 40, 130, z0, z0 + 60),
                         "#15803D", 7, (760, 0, 860))

    # 8 tiller head replacing the grip, with belly-reverse paddle; 12 beacon on top of it
    hw = P["head_w"]
    out["tiller"] = ("Tiller control head",
                     Pos(tx + 20, 0, tz - 30) * Box(90, hw, 110) + box(tx + 60, tx + 90, -60, 60, tz - 90, tz - 20),
                     "#1F2937", 8, (260, 0, 120))
    out["beacon"] = ("Status beacon and buzzer", Pos(tx + 20, 70, tz + 25 + 30) * Cylinder(22, 60), "#38BDF8", 12, (260, 0, 260))

    # 9 emergency stops: tiller head top, enclosure rear face (toward the operator in follow mode)
    out["estop"] = ("Emergency stops (2)", Pos(ex1 + 14, -80, 270) * Rot(0, 90, 0) * Cylinder(20, 28), "#DC2626", 9, (720, 0, 260))
    out["estop_head"] = ("Emergency stop, tiller", Pos(tx + 10, -40, tz + 25 + 11) * Cylinder(20, 22), "#DC2626", None, (260, 0, 120))

    # 10 contact bumper: U hoop with safety edge on the front face and side arms
    bx = D["bumper_face_x"]
    bh = P["bumper_half_w"]
    b0, b1, ed = P["bumper_z0"], P["bumper_z1"], P["edge_depth"]
    bumper = (box(bx - ed, bx, -bh, bh, b0, b1)
              + box(P["bumper_x0"], bx - ed, bh - 40, bh, b0, b1) + box(P["bumper_x0"], bx - ed, -bh, -bh + 40, b0, b1))
    out["bumper"] = ("Contact bumper (safety edge)", bumper, "#F59E0B", 10, (420, 0, 0))
    out["bumper_mounts"] = ("Bumper mounts",
                            box(P["cheek_x1"] - 20, bx - ed, hy + 2 * t, bh - 40, 110, 130)
                            + box(P["cheek_x1"] - 20, bx - ed, -bh + 40, -hy - 2 * t, 110, 130),
                            "#6B7280", None, (420, 0, 0))

    # 11 UWB anchors: two bumper corners (baseline 2 x anchor_y), one on the tiller head
    ay, at = P["anchor_y"], P["anchor_top"]
    out["anchor_a"] = ("UWB anchors (3)", box(bx - 40, bx - 5, -ay - 18, -ay + 18, b1, at), "#7C3AED", 11, (560, 0, 0))
    out["anchor_b"] = ("UWB anchor, right", box(bx - 40, bx - 5, ay - 18, ay + 18, b1, at), "#7C3AED", None, (560, 0, 0))
    out["anchor_head"] = ("UWB anchor, tiller", box(tx - 5, tx + 35, -hw / 2 - 35, -hw / 2, tz - 40, tz), "#7C3AED", None, (260, 0, 120))

    # 13 manual release lever on the enclosure side
    out["release"] = ("Manual release lever",
                      box(ex0 + 20, ex1 - 40, -ey - 30, -ey - 10, 250, 270) + box(ex1 - 60, ex1 - 40, -ey - 30, -ey, 240, 280),
                      "#E5E7EB", 13, (620, -260, 260))

    # 18 obstacle lidar on a bracket from the subframe, scan plane above the bumper and anchors
    lx = D["lidar_x"]
    lz0 = P["lidar_scan_z"] - P["lidar_h"] / 2
    lidar = Pos(lx, 0, lz0 + P["lidar_h"] / 2) * Cylinder(P["lidar_d"] / 2, P["lidar_h"])
    bracket = box(P["plate_x1"] - 20, lx + 20, -35, 35, lz0 - 6, lz0) + box(P["plate_x1"] - 20, P["plate_x1"], -35, 35, lz0 - 6, P["plate_z"])
    out["lidar"] = ("Obstacle lidar and bracket", lidar + bracket, "#0EA5E9", 18, (700, 0, 60))
    return out


def kit_keys(parts):
    return [k for k in parts if k != "donor"]


def build(P=PARAMS, with_donor=True):
    """Assembly as one Compound."""
    from build123d import Compound
    parts = build_parts(P)
    keys = list(parts) if with_donor else kit_keys(parts)
    return Compound(children=[parts[k][1] for k in keys])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    groups = {
        "palletpilot-assembly": list(parts),
        "palletpilot-kit": kit_keys(parts),
        "drive-module": ["subframe", "motors"],
        "enclosure": ["enclosure", "lid", "pack", "driver", "contactor", "controller", "estop", "release"],
        "bumper-and-sensors": ["bumper", "bumper_mounts", "anchor_a", "anchor_b", "lidar"],
        "tiller-head": ["tiller", "beacon", "estop_head", "anchor_head"],
    }
    for name, keys in groups.items():
        c = Compound(children=[parts[k][1] for k in keys])
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
    D = derived()
    print("exported STEP and STL to cad/step and cad/stl:", ", ".join(groups))
    print(f"bumper face X {D['bumper_face_x']:.0f} mm; added length {D['added_length']:.0f} mm; "
          f"handle clearance at 90 deg {D['handle_clear_90']:.0f} mm; anchor baseline {D['anchor_baseline']:.0f} mm")
