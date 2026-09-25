"""PalletPilot concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the truck, fork tips toward -X and the handle end toward +X; Y across the
forks; Z up from the floor. Units mm. The donor is a common 27 x 48 in (685 x 1220 mm)
manual pallet jack with a 75 mm (3 in) lowered fork height. Donor parts are grey and carry
no BOM number; kit parts are colored and numbered to match bom/bom.csv.

Everything in the kit (drive module, battery box, bumper, anchors) hangs off the donor's
steering yoke, so it turns with the handle and never sits on the forks where the pallet goes.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def wheel(x, y, z, r, w):
    """Wheel with its axle along Y."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


# ---------------------------------------------------------------- donor manual pallet jack
FORK_L, FORK_W, FORK_H = 1160.0, 160.0, 55.0     # fork channel length, width, depth
OUT_W = 685.0                                    # outside width over forks (27 in)
FORK_TOP = 80.0                                  # lowered fork height, about 3 in
X_TIP = -1220.0                                  # fork tips (48 in forks)
fy = OUT_W / 2 - FORK_W / 2                      # fork centerline, about 262 mm
forks = (box(X_TIP, X_TIP + FORK_L, fy - FORK_W / 2, fy + FORK_W / 2, FORK_TOP - FORK_H, FORK_TOP)
         + box(X_TIP, X_TIP + FORK_L, -fy - FORK_W / 2, -fy + FORK_W / 2, FORK_TOP - FORK_H, FORK_TOP))
load_rollers = (wheel(X_TIP + 90, fy, 40, 40, 110) + wheel(X_TIP + 90, -fy, 40, 40, 110))
frame_head = box(-60, 40, -OUT_W / 2, OUT_W / 2, 25, 230)            # rear frame joining the forks
pump = Pos(110, 0, 250) * Cylinder(55, 200)                           # hydraulic pump on the yoke
yoke = box(60, 160, -110, 110, 150, 175)                              # steering yoke plate
steer_wheels = wheel(110, 72, 90, 90, 50) + wheel(110, -72, 90, 90, 50)

# handle: pivot on the pump, leaning 20 degrees toward +X, 900 mm long
PIV = (110.0, 350.0)
ANG = math.radians(20)
H_LEN = 900.0
hx, hz = PIV[0] + H_LEN / 2 * math.sin(ANG), PIV[1] + H_LEN / 2 * math.cos(ANG)
shaft = Pos(hx, 0, hz) * Rot(0, 20, 0) * Cylinder(16, H_LEN)
TOPX, TOPZ = PIV[0] + H_LEN * math.sin(ANG), PIV[1] + H_LEN * math.cos(ANG)
loop = (Pos(TOPX, 0, TOPZ + 20) * Rot(0, 90, 0) * Cylinder(14, 60)
        + box(TOPX - 15, TOPX + 15, -150, 150, TOPZ + 10, TOPZ + 40))
donor = forks + load_rollers + frame_head + pump + yoke + steer_wheels + shaft + loop

# ---------------------------------------------------------------- kit parts (BOM numbers)
# 1 Drive module subframe: clamp plate on the yoke, trailing arm, spring preload towers
DX = 330.0                                            # drive axle X
subframe = (box(150, 400, -175, 175, 205, 225)        # top plate
            + box(150, 170, -60, 60, 175, 205)        # clamp to the yoke
            + box(260, 400, 150, 165, 100, 205)       # side cheeks carrying the axle
            + box(260, 400, -165, -150, 100, 205))
springs = Pos(200, 110, 190) * Cylinder(18, 30) + Pos(200, -110, 190) * Cylinder(18, 30)
subframe = subframe + springs

# 2 Two 200 mm (8 in) 24 V hub motors with spring-applied brakes, driven differentially
drive_wheels = wheel(DX, 110, 100, 100, 60) + wheel(DX, -110, 100, 100, 60)

# 3 Battery and electronics enclosure (shell) on the subframe
EX0, EX1, EY, EZ0, EZ1, T = 175.0, 455.0, 150.0, 225.0, 395.0, 3.0
enclosure = box(EX0, EX1, -EY, EY, EZ0, EZ1) - box(EX0 + T, EX1 - T, -EY + T, EY - T, EZ0 + T, EZ1 + 1)
lid = box(EX0, EX1, -EY, EY, EZ1, EZ1 + 8)

# 4 24 V (25.6 V) 20 Ah LiFePO4 pack with BMS, inside the enclosure
pack = box(EX0 + 10, 330, -135, 135, EZ0 + 5, EZ0 + 130)
# 5 Dual-channel motor driver
driver = box(340, EX1 - 10, -120, 30, EZ0 + 5, EZ0 + 60)
# 6 Main contactor, fuse and disconnect
contactor = box(350, 420, 50, 120, EZ0 + 5, EZ0 + 75) + Pos(385, 150 + 18, 330) * Rot(90, 0, 0) * Cylinder(22, 30)
# 7 Controller board (ESP32-S3 class) with CAN and the safety relay beside it
mcu = box(345, 440, -120, 20, EZ0 + 70, EZ0 + 90) + box(345, 440, 40, 130, EZ0 + 85, EZ0 + 140)

# 8 Tiller control head replacing the grip: thumb throttle, belly-reverse paddle, mode key, horn
th = (Pos(TOPX + 20, 0, TOPZ - 30) * Box(90, 220, 110)
      + box(TOPX + 60, TOPX + 90, -60, 60, TOPZ - 90, TOPZ - 20))       # belly-reverse paddle
# 9 Emergency stops: one on the control head, one on the enclosure lid
estop_lid = Pos(420, -90, EZ1 + 8 + 14) * Cylinder(22, 28)
estop_head = Pos(TOPX + 10, 0, TOPZ + 40) * Cylinder(20, 22)

# 10 Contact bumper: pressure-sensitive safety edge on a U-shaped hoop around the drive end
BX = 500.0
bumper = (box(BX - 40, BX + 30, -240, 240, 50, 150)
          + box(170, BX - 40, 200, 240, 50, 150) + box(170, BX - 40, -240, -200, 50, 150))
bumper_mounts = box(380, 460, 160, 200, 120, 140) + box(380, 460, -200, -160, 120, 140)

# 11 UWB anchors: two on the bumper corners (about 450 mm baseline), one on the control head
anchor_a = box(BX - 30, BX + 10, -245, -205, 150, 185)
anchor_b = box(BX - 30, BX + 10, 205, 245, 150, 185)
anchor_head = box(TOPX - 5, TOPX + 35, -140, -100, TOPZ + 12, TOPZ + 50)

# 12 Status beacon and buzzer on the lid
beacon = Pos(220, 110, EZ1 + 8 + 30) * Cylinder(26, 60)

# 13 Manual release: lever that lifts the drive wheels clear and frees the brakes
release = box(390, 410, -20, 20, EZ1 + 8, EZ1 + 58) + Pos(400, 0, EZ1 + 70) * Rot(90, 0, 0) * Cylinder(10, 90)

parts = [
    Part("Donor manual pallet jack (not in kit)", donor, "#9CA3AF", None),
    Part("Drive module subframe and preload springs", subframe, "#374151", 1, (0, 0, 160)),
    Part("Hub motors, 24 V, 200 mm, with brakes", drive_wheels, "#111827", 2, (0, -420, 0)),
    Part("Battery and electronics enclosure", enclosure, "#0F766E", 3, (700, 0, 180)),
    Part("LiFePO4 pack 25.6 V 20 Ah with BMS", pack, "#D4A017", 4, (700, 0, 470)),
    Part("Dual-channel motor driver", driver, "#B45309", 5, (820, 0, 700)),
    Part("Contactor, fuse and disconnect", contactor, "#991B1B", 6, (820, 0, 860)),
    Part("Controller and safety relay", mcu, "#15803D", 7, (820, 0, 1000)),
    Part("Tiller control head", th, "#1F2937", 8, (260, 0, 120)),
    Part("Emergency stops (2)", estop_lid, "#DC2626", 9, (700, 0, 1180)),
    Part("Emergency stop, tiller", estop_head, "#DC2626", None, (260, 0, 120)),
    Part("Contact bumper (safety edge)", bumper, "#F59E0B", 10, (420, 0, 0)),
    Part("Bumper mounts", bumper_mounts, "#6B7280", None, (420, 0, 0)),
    Part("UWB anchors (3)", anchor_a, "#7C3AED", 11, (650, 0, 0)),
    Part("UWB anchor, right", anchor_b, "#7C3AED", None, (650, 0, 0)),
    Part("UWB anchor, tiller", anchor_head, "#7C3AED", None, (260, 0, 120)),
    Part("Status beacon and buzzer", beacon, "#38BDF8", 12, (600, -220, 1260)),
    Part("Enclosure lid", lid, "#115E59", None, (700, 0, 1180)),
    Part("Manual release lever", release, "#E5E7EB", 13, (820, 150, 1330)),
]

# Context for the hero render only: a 48 x 40 in stringer pallet with cartons over the forks
PX0, PX1 = -1225.0, -5.0
pallet = (box(PX0, PX1, -508, 508, 118, 140)                           # top deck
          + box(PX0, PX1, -508, -470, 0, 118) + box(PX0, PX1, -19, 19, 0, 118)
          + box(PX0, PX1, 470, 508, 0, 118))                          # three stringers
cartons = box(PX0 + 20, PX1 - 20, -490, 490, 140, 700)
context = [Part("Pallet", pallet, "#C8A97E"), Part("Cartons, about 1,000 kg", cartons, "#D6C3A0")]

render_all(
    parts, project="PalletPilot", title="Pallet jack retrofit concept", dwg_no="PLP-DWG-010",
    key_figures=["Design load 1,000 kg; kit rating 1,500 kg (proposed)",
                 "Walk mode up to 1.2 m/s; follow mode up to 0.6 m/s",
                 "Rolling force about 130 N loaded (estimate)",
                 "Pack 25.6 V 20 Ah: 410 Wh usable, shift uses 281 Wh (est.)",
                 "Stop from 0.6 m/s loaded: about 0.42 m (estimate)",
                 "Kit about 37 kg; about $1,425 in parts (estimates)"],
    context=context, cut_exclude=("Contact bumper (safety edge)", "Bumper mounts", "UWB anchors (3)", "UWB anchor, right"),
    flow={"title": "energy per 8 h shift, 60 pallet moves (all values are estimates)", "unit": "Wh",
          "stages": [("Wall outlet (AC)", 336), ("Pack, delivered", 281), ("Motor driver input", 217),
                     ("Work at the wheels", 152)],
          "losses": [(0, "Charging (est.)", 55), (1, "Controls (est.)", 64),
                     (2, "Motors (est.)", 65)]},
)
