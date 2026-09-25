"""PalletPilot sizing calculations for PLP-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that PLP-CAL-001 quotes. Tags in brackets, for example [F3],
match the tags in the note. Geometry comes from cad/src/model.py (PARAMS, derived),
so the note, the model and drawing PLP-DWG-001 use the same dimensions.
Prices come from bom/bom.csv.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

G = 9.81
D = derived(P)
rows = []          # (tag, text) for the printout


def out(tag, text):
    rows.append((tag, text))
    print(f"[{tag}] {text}")


# ------------------------------------------------------------------ A. assumptions
A = dict(
    pallet=1000.0, pallet_max=1500.0, jack=64.0,
    crr=0.012, cbreak=0.025, grade=0.02,
    mu=0.5, mu_low=0.4,
    preload=1500.0,            # N, spring preload on the two drive wheels together (TRL 2 value was 1,100 N)
    r=P["drive_r"] / 1000,     # m
    t_peak=30.0,               # N m per motor, specified minimum peak torque
    t_rated=12.0,              # N m per motor, specified minimum continuous torque
    t_brake=20.0,              # N m per motor, specified minimum spring-brake dynamic torque
    a_level=0.30, a_ramp=0.10, a_heavy=0.20,   # m/s2 acceleration settings
    v_walk=1.2, v_forks=0.8, v_creep=0.3, v_follow=0.6, v_bumper=0.2,
    eff_drive=0.70, p_ctrl=9.2, shift_h=8.0, soc_use=0.80, eff_cell=0.95, eff_chg=0.88,
    pack_v=25.6, pack_ah=20.0, chg_a=5.0, cv_h=0.5,
    moves=60, dist=40.0, starts=4,
    td_lidar=0.25, td_bumper=0.10, td_tag=0.20,
    field_margin=0.10, sigma_r=0.10, uwb_hz=20.0, window_s=0.5, bias_r=0.03,
    gap=1.5, gap_tol=0.3, tag_to_legs=0.15,
    pallet_cg_x=-615.0, jack_rear_share=0.45,
)

# ------------------------------------------------------------------ B. mass
steel, alu = 7850.0, 2680.0
top_plate = (P["plate_x1"] - P["plate_x0"]) / 1e3 * 2 * P["plate_half_w"] / 1e3 * P["plate_t"] / 1e3 * steel
cheeks = 2 * (P["cheek_x1"] - P["cheek_x0"]) / 1e3 * 0.135 * 2 * P["plate_t"] / 1e3 * steel
clamp_hw = 2.5                                              # clamp block, tongue, bolts, spring towers, axle clamps
subframe = top_plate + cheeks + clamp_hw
ex = (P["enc_x1"] - P["enc_x0"]) / 1e3; ey = 2 * P["enc_half_w"] / 1e3; ez = (P["enc_top"] - P["enc_z0"]) / 1e3
enclosure = 2 * (ex * ey + ex * ez + ey * ez) * 0.002 * alu + 0.3   # 2 mm aluminium plus hinges and glands
pack = 48 * 0.085 + 0.8                                     # 8S6P 26650 cells at 85 g plus BMS and case
hoop_len = 2 * (D["bumper_face_x"] - P["edge_depth"] - P["bumper_x0"]) / 1e3 + 2 * P["bumper_half_w"] / 1e3
bumper = hoop_len * 1.76 + 1.3 * 0.6 + 0.8                  # 40 x 20 x 2 tube, edge profile, mounts
masses = {
    "1 Subframe and springs": subframe, "2 Hub motors (2 x 7.0 kg)": 14.0, "3 Enclosure (aluminium)": enclosure,
    "4 Pack with BMS": pack, "5 Motor driver": 1.0, "6 Contactor, fuse, disconnect": 0.8,
    "7 Controller and safety relay": 0.4, "8 Tiller head": 1.5, "9 Emergency stops": 0.2, "10 Bumper": bumper,
    "11 UWB anchors": 0.15, "12 Beacon": 0.2, "13 Release lever": 0.8, "16 Handle sensor and gas spring": 0.5,
    "17 Wiring and hardware": 2.0, "18 Lidar and bracket": 0.5,
}
kit = sum(masses.values())
for k, v in masses.items():
    out("B0", f"mass {k}: {v:.2f} kg")
out("B1", f"kit mass on the truck {kit:.1f} kg (charger and tag not carried); R15 target 40 kg")
m = A["pallet"] + A["jack"] + kit
m_heavy = A["pallet_max"] + A["jack"] + kit
m_empty = A["jack"] + kit
out("B2", f"design total {m:.0f} kg; with 1,500 kg pallet {m_heavy:.0f} kg; empty {m_empty:.0f} kg")

# ------------------------------------------------------------------ C. axle loads and preload
span = P["kingpin_x"] - P["load_roller_x"]
share = (A["pallet_cg_x"] - P["load_roller_x"]) / span
yoke = lambda pallet: (pallet * share + A["jack"] * A["jack_rear_share"] + kit) * G
out("C1", f"pallet share on the steer axle {share:.3f}; yoke ground load {yoke(A['pallet'])/1e3:.2f} kN at 1,000 kg, "
          f"{yoke(A['pallet_max'])/1e3:.2f} kN at 1,500 kg, {yoke(0)/1e3:.2f} kN empty")
out("C2", f"steer wheels keep {(yoke(A['pallet']) - A['preload'])/1e3:.2f} kN at 1,000 kg with {A['preload']/1e3:.1f} kN preload")
out("C3", f"empty: yoke load {yoke(0)/1e3:.2f} kN is below the preload, so the steer wheels unload and the drive "
          f"wheels carry the yoke; empty traction {A['mu']*yoke(0):.0f} N for {m_empty:.0f} kg ({A['mu']*yoke(0)/(m_empty*G):.2f} g)")
bearing = (A["pallet"] * share + A["jack"] * A["jack_rear_share"]) * G
bearing_h = (A["pallet_max"] * share + A["jack"] * A["jack_rear_share"]) * G
bearing_donor = (2500 * share + A["jack"] * A["jack_rear_share"]) * G
out("C4", f"steering bearing vertical load {bearing/1e3:.2f} kN (1,000 kg), {bearing_h/1e3:.2f} kN (1,500 kg), "
          f"{bearing_donor/1e3:.2f} kN at the donor's 2,500 kg rating; kit adds up to {A['mu']*A['preload']:.0f} N horizontal")

# ------------------------------------------------------------------ F. forces, traction, torque
T = A["mu"] * A["preload"]; T_low = A["mu_low"] * A["preload"]
f_roll = m * G * A["crr"]; f_break = m * G * A["cbreak"]; f_grade = m * G * A["grade"]
out("F1", f"rolling {f_roll:.0f} N; breakaway {f_break:.0f} N; 2 % grade {f_grade:.0f} N (design total)")
out("F2", f"available traction {T:.0f} N at mu {A['mu']}, {T_low:.0f} N at mu {A['mu_low']}")
cases = {
    "level start (breakaway)": f_break,
    "level, accelerate 0.3 m/s2": f_roll + m * A["a_level"],
    "2 % ramp start (breakaway plus grade)": f_break + f_grade,
    "2 % ramp, accelerate 0.1 m/s2": f_roll + f_grade + m * A["a_ramp"],
    "1,500 kg level, accelerate 0.2 m/s2": m_heavy * G * A["crr"] + m_heavy * A["a_heavy"],
    "1,500 kg, 2 % ramp start": m_heavy * G * (A["cbreak"] + A["grade"]),
}
f_need = max(v for k, v in cases.items() if k != "1,500 kg, 2 % ramp start")
for k, v in cases.items():
    out("F3", f"{k}: {v:.0f} N; {v*A['r']/2:.1f} N m per motor; traction margin {T/v:.2f} (mu 0.5), {T_low/v:.2f} (mu 0.4)")
out("F4", f"worst case within R2 and R3 needs {f_need*A['r']/2:.1f} N m per motor against {A['t_peak']:.0f} N m specified peak; "
          f"a 1,500 kg ramp start needs {cases['1,500 kg, 2 % ramp start']*A['r']/2:.1f} N m, so the 1,500 kg rating is for level floors only")
t_cont = f_roll * A["r"] / 2
rpm = A["v_walk"] / (2 * math.pi * A["r"]) * 60
out("F5", f"continuous at 1.2 m/s level: {t_cont:.1f} N m per motor (spec {A['t_rated']:.0f} N m); wheel speed {rpm:.0f} rpm")
p_peak = (f_roll + m * A["a_level"]) * A["v_walk"]
i_peak = p_peak / A["eff_drive"] / A["pack_v"]
out("F6", f"peak wheel power {p_peak:.0f} W at 1.2 m/s while accelerating; pack current {i_peak:.0f} A "
          f"(about {i_peak/2:.0f} A per channel); cruise {f_roll*A['v_walk']:.0f} W")
# steering by differential drive: yaw moment about the steering axis
trail = D["trail"] / 1000; half_track = P["drive_track"] / 2000
m_avail = 2 * (T / 2) * half_track
m_scrub = A["mu"] * A["preload"] * trail
out("F7", f"drive axle {D['trail']:.0f} mm ahead of the steering axis; differential yaw moment available {m_avail:.0f} N m; "
          f"static scrub to swing the yoke {m_scrub:.0f} N m, so the yoke cannot be swung at standstill by the motors")
out("F8", f"standstill hand steering adds about {m_scrub/1.2:.0f} N at a 1.2 m handle (wheels lowered); rolling, it falls to wheel slip only")

# ------------------------------------------------------------------ S. stopping
f_ctrl = min(2 * A["t_peak"] / A["r"], T)
f_ebrk = min(2 * A["t_brake"] / A["r"], T)
out("S1", f"controlled stop force {f_ctrl:.0f} N (motor peak torque limit); spring-brake stop force {f_ebrk:.0f} N")


def stop(v, mass, force, td, grade=0.0):
    a = (force + mass * G * A["crr"] - mass * G * grade) / mass
    return v * td + v * v / (2 * a), a


stops = [
    ("walk 1.2 m/s, controlled, level", A["v_walk"], m, f_ctrl, A["td_bumper"], 0),
    ("walk 1.2 m/s, e-stop (brakes), level", A["v_walk"], m, f_ebrk, A["td_bumper"], 0),
    ("walk 1.2 m/s, e-stop, 2 % downgrade", A["v_walk"], m, f_ebrk, A["td_bumper"], A["grade"]),
    ("follow 0.6 m/s, lidar stop, level", A["v_follow"], m, f_ctrl, A["td_lidar"], 0),
    ("follow 0.6 m/s, lidar stop, 2 % downgrade", A["v_follow"], m, f_ctrl, A["td_lidar"], A["grade"]),
    ("follow 0.6 m/s, lidar stop, 1,500 kg, 2 % downgrade", A["v_follow"], m_heavy, f_ctrl, A["td_lidar"], A["grade"]),
    ("follow 0.6 m/s, bumper only, level", A["v_follow"], m, f_ebrk, A["td_bumper"], 0),
    ("creep 0.3 m/s, bumper only, level", A["v_creep"], m, f_ebrk, A["td_bumper"], 0),
    ("0.2 m/s, bumper only, level", A["v_bumper"], m, f_ebrk, A["td_bumper"], 0),
]
res = {}
for name, v, mass, f, td, gr in stops:
    s, a = stop(v, mass, f, td, gr)
    res[name] = s
    out("S2", f"{name}: decel {a:.2f} m/s2, stop {s:.3f} m, energy {0.5*mass*v*v:.0f} J")
# bumper-only speed that stops within the edge travel, level, spring brakes
a_e = (f_ebrk + m * G * A["crr"]) / m
tr = P["edge_travel"] / 1000
v_b = (-A["td_bumper"] + math.sqrt(A["td_bumper"] ** 2 + 2 * tr / a_e)) * a_e
out("S3", f"bumper-only speed that stops within {P['edge_travel']:.0f} mm travel: {v_b:.2f} m/s; "
          f"at 0.2 m/s the edge would need {res['0.2 m/s, bumper only, level']*1000:.0f} mm")
need_travel_02 = res["0.2 m/s, bumper only, level"] * 1000
field = max(res[k] for k in res if "lidar" in k) + A["field_margin"]
limit = A["gap"] - A["gap_tol"] - A["tag_to_legs"]
out("S4", f"lidar protective field length {field:.2f} m ahead of the bumper face (worst lidar stop plus {A['field_margin']} m); "
          f"nearest operator legs at about {limit:.2f} m, so the field stays clear of the operator by {limit-field:.2f} m")
out("S5", f"lidar lateral field: truck width {P['out_w']:.0f} mm plus 100 mm each side = {P['out_w']+200:.0f} mm")
out("S6", f"tag loss: timeout 3 missed frames at {A['uwb_hz']:.0f} Hz plus command = {A['td_tag']:.2f} s to stop command (R6 target 0.3 s)")
hold = f_grade
out("S7", f"parking on 2 %: needs {hold:.0f} N = {hold*A['r']:.1f} N m total; spring brakes give {2*A['t_brake']:.0f} N m "
          f"(margin {2*A['t_brake']/(hold*A['r']):.2f})")

# ------------------------------------------------------------------ U. UWB error budget
b = D["anchor_baseline"] / 1000
s_raw = math.degrees(math.sqrt(2) * A["sigma_r"] / b)
n = A["uwb_hz"] * A["window_s"]
s_filt = s_raw / math.sqrt(n)
s_bias = math.degrees(math.sqrt(2) * A["bias_r"] / b)
s_tot = math.hypot(s_filt, s_bias)
out("U1", f"anchor baseline {b*1000:.0f} mm; raw bearing error {s_raw:.1f} deg (1 sigma), {2*s_raw:.1f} deg (2 sigma)")
out("U2", f"filtered over {n:.0f} samples: {s_filt:.1f} deg; correlated error ({A['bias_r']*100:.0f} cm per range) {s_bias:.1f} deg; "
          f"total {s_tot:.1f} deg (1 sigma), {2*s_tot:.1f} deg (2 sigma) against +/-10 deg")
b_need = math.sqrt(2) * math.hypot(A["sigma_r"] / math.sqrt(n), A["bias_r"]) * 2 / math.radians(10)
out("U3", f"baseline needed for +/-10 deg at 2 sigma with the same filter: {b_need*1000:.0f} mm (truck width {P['out_w']:.0f} mm)")
out("U4", f"lateral error at the 1.5 m gap: {A['gap']*math.tan(math.radians(2*s_tot)):.2f} m (2 sigma); "
          f"gap error {2*A['sigma_r']/math.sqrt(n):.2f} m (2 sigma) against +/-0.3 m")

# ------------------------------------------------------------------ E. energy and charging
def move_work(mass):
    return mass * G * A["crr"] * A["dist"] + A["starts"] * 0.5 * mass * A["v_walk"] ** 2


w_move = move_work(m) + move_work(m_empty)
w_wheels = A["moves"] * w_move / 3600
w_drive = w_wheels / A["eff_drive"]
w_ctrl = A["p_ctrl"] * A["shift_h"]
w_pack = w_drive + w_ctrl
usable = A["pack_v"] * A["pack_ah"] * A["soc_use"]
w_wall = w_pack / A["eff_cell"] / A["eff_chg"]
t_chg = A["pack_ah"] / A["chg_a"] + A["cv_h"]
out("E1", f"work at the wheels {w_wheels:.0f} Wh ({w_move/3600:.2f} Wh per move); driver input {w_drive:.0f} Wh; "
          f"controls, UWB, lidar and lights {w_ctrl:.0f} Wh")
out("E2", f"from the pack {w_pack:.0f} Wh of {usable:.0f} Wh usable; left {(usable-w_pack)/usable*100:.0f} % (R12 needs 20 %)")
out("E3", f"from the wall {w_wall:.0f} Wh; charge time {t_chg:.1f} h at {A['chg_a']:.0f} A (R13 target 5 h)")
out("E4", f"losses: charging {w_wall-w_pack:.0f} Wh, controls {w_ctrl:.0f} Wh, motors and driver {w_drive-w_wheels:.0f} Wh")

# ------------------------------------------------------------------ G. geometry
a70 = math.radians(70)
x_front = P["enc_x0"]
clr70 = P["pivot_z"] + (x_front - P["kingpin_x"]) / math.tan(a70) - P["handle_r"] / math.sin(a70) - P["enc_top"]
out("G1", f"handle clearance over the enclosure: {clr70:.0f} mm at 70 deg, {D['handle_clear_90']:.0f} mm with the handle horizontal")
out("G2", f"added length at floor level {D['added_length']:.0f} mm (bumper face X {D['bumper_face_x']:.0f}, bare jack rear X "
          f"{D['bare_rear_x']:.0f}); overall {D['overall_len']:.0f} mm against {D['bare_len']:.0f} mm bare")
out("G3", f"drive wheel tread to rigid hoop {P['bumper_clear']:.0f} mm; lidar scan plane {P['lidar_scan_z']:.0f} mm above the floor, "
          f"above the hoop ({P['bumper_z1']:.0f}) and anchors ({P['anchor_top']:.0f})")
throw, lever, eff = 25.0, 400.0, 0.8
out("G4", f"release lever effort {A['preload']*throw/(lever*eff):.0f} N (cam throw {throw:.0f} mm, lever {lever:.0f} mm, 80 % efficiency); "
          f"unpowered rolling force rises {kit/(A['pallet']+A['jack'])*100:.1f} % with the drive wheels lifted (R14 limit 10 %)")

# ------------------------------------------------------------------ K. cost
with open(ROOT / "bom" / "bom.csv") as f:
    bom = list(csv.DictReader(f))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
out("K1", f"BOM total ${total:,.0f} over {len(bom)} lines against budget $1,550 ({(total/1550-1)*100:+.1f} %)")

# ------------------------------------------------------------------ R. requirement table
status = [
    ("R1", "Fits common jacks; bolt-on; fit 2 h, remove 1 h", "Clamp to yoke, no drilling; donor geometry assumed", "Not verifiable at TRL 3"),
    ("R2", "Move 1,000 kg; rating 1,500 kg at 0.8 m/s or less",
     f"{cases['level, accelerate 0.3 m/s2']*A['r']/2:.1f} and {cases['1,500 kg level, accelerate 0.2 m/s2']*A['r']/2:.1f} N m per motor of 30; traction {T:.0f} N", "Met"),
    ("R3", "Start, climb, hold on 2 %", f"start needs {cases['2 % ramp start (breakaway plus grade)']:.0f} N of {T:.0f} N (margin {T/cases['2 % ramp start (breakaway plus grade)']:.2f}); hold margin {2*A['t_brake']/(hold*A['r']):.2f}", "Met"),
    ("R4", "Speed limits", "1.2, 0.8, 0.3, 0.6 m/s set in the controller", "Met"),
    ("R5", "Gap +/-0.3 m, bearing +/-10 deg", f"gap +/-{2*A['sigma_r']/math.sqrt(n):.2f} m; bearing +/-{2*s_tot:.0f} deg (2 sigma)", "Not met"),
    ("R6", "Stop within 0.3 s of tag loss", f"timing budget {A['td_tag']:.2f} s; firmware not written", "Not verifiable at TRL 3"),
    ("R7", "Stop without contact from 0.6 m/s (lidar layer)", f"stop {max(res[k] for k in res if 'lidar' in k):.2f} m inside a {field:.2f} m field; sensor not safety-rated", "At risk"),
    ("R8", "Bumper stop in 100 ms; bumper-only 0.2 m/s or less", f"0.10 s chain; 0.2 m/s needs {need_travel_02:.0f} mm travel vs {P['edge_travel']:.0f} mm; {v_b:.2f} m/s fits", "At risk"),
    ("R9", "Hardwired stops, PL d", "Dual-channel relay, one contactor; PL not calculated", "At risk"),
    ("R10", "Brakes hold 2 % with power off", f"{2*A['t_brake']:.0f} N m spec vs {hold*A['r']:.1f} N m", "Met"),
    ("R11", "Handle 20 to 70 deg band; belly reverse", f"handle clears the enclosure by {clr70:.0f} mm at 70 deg, {D['handle_clear_90']:.0f} mm at 90 deg", "Met"),
    ("R12", "Shift with 20 % left", f"{w_pack:.0f} of {usable:.0f} Wh; {(usable-w_pack)/usable*100:.0f} % left", "Met"),
    ("R13", "Charge in 5 h or less", f"{t_chg:.1f} h", "Met"),
    ("R14", "Push by hand; 10 s release; +10 % force max", f"+{kit/(A['pallet']+A['jack'])*100:.1f} %; lever {A['preload']*throw/(lever*eff):.0f} N", "Met"),
    ("R15a", "Kit mass 40 kg or less", f"{kit:.1f} kg", "Not met" if kit > 40 else "Met"),
    ("R15b", "Added length 300 mm or less", f"{D['added_length']:.0f} mm", "Met" if D["added_length"] <= 300 else "Not met"),
    ("R16", "0 to 40 degC, IP54, no charge below 0 degC", "By specification of bought parts", "Not verifiable at TRL 3"),
    ("R17", "Kit parts $1,550 or less", f"${total:,.0f}", "Met" if total <= 1550 else "Not met"),
]
print()
for r in status:
    out("R", " | ".join(r))
from collections import Counter
c = Counter(s for *_, s in status)
out("R0", ", ".join(f"{k}: {v}" for k, v in sorted(c.items())))
