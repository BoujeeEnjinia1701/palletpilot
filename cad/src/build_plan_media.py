"""PalletPilot prototype build plan pictures (PLP-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/PLP-DWG-101 to 111        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level power and stop-chain wiring (matplotlib)
A single sheet or picture can be drawn on its own, for example "sheets 103" or "steps 7", to keep
memory low. Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, release_state, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = build_components(P)

COL = {k: c.color for k, c in C.items()}
COL.update({"subframe": "#475569", "jaw": "#1E3A8A", "arms": "#0F766E", "pin": "#B45309", "cam": "#1D4ED8",
            "spring": "#D4A017", "saddle": "#A16207", "strap": "#78716C", "lever": "#DC2626", "link": "#6D28D9",
            "enc": "#0F766E", "hoop": "#F59E0B", "edge": "#1F2937", "bolt": "#111827", "stops": "#57534E",
            "donor": "#D6D3D1"})


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def side(shape, sgn):
    """The half of a mirrored component on one side (sgn +1 right, -1 left)."""
    return shape & box(-2000, 2000, 0 if sgn > 0 else -2000, 2000 if sgn > 0 else 0, -500, 2000)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & box(x0, x1, y0, y1, z0, z1)


def donor_yoke():
    return part("Jack yoke, pump and steer wheels (donor)", C["donor_yoke"].shape & box(-200, 400, -400, 400, -10, 345), COL["donor"])


def donor_head():
    return part("Jack frame head (donor)", C["donor_fixed"].shape & box(-200, 20, -400, 400, 0, 260), COL["donor"])


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "subframe": part("Subframe (top plate and welded hangers)", C["subframe"].shape, COL["subframe"]),
        "stops": part("Steering stops (2)", C["steer_stops"].shape, COL["stops"]),
        "cam": part("Cam shaft, cams and crank", C["camshaft"].shape, COL["cam"]),
        "jaw": part("Lower jaw, packing bar and M12 bolts", S("jaw", "clamp_bolts"), COL["jaw"]),
        "motors": part("Hub motors (2)", C["motors"].shape, "#111827"),
        "arms": part("Drive arms (2)", S("arm_r", "arm_l"), COL["arms"]),
        "pin": part("Pivot tubes, spacers and bolts", C["pivot_pin"].shape, COL["pin"]),
        "springs": part("Springs, saddles and lift straps", S("springs", "saddles", "straps"), COL["spring"]),
        "lever": part("Release lever, link and pins", S("lever", "link", "lever_pins"), COL["lever"]),
        "enc": part("Enclosure with feet and M8 bolts", S("enclosure", "feet", "feet_bolts"), COL["enc"]),
        "inside": part("Pack, driver, contactors, controller, rear stop", S("pack", "driver", "contactor", "controller", "estop"), "#D4A017"),
        "lid": part("Enclosure lid", C["lid"].shape, "#115E59"),
        "hoop": part("Bumper hoop and M8 bolts", S("hoop", "hoop_bolts"), COL["hoop"]),
        "edge": part("Safety edge", C["edge"].shape, COL["edge"]),
        "lidar": part("Safety scanner and its shelf", S("lidar", "lidar_bracket"), "#0EA5E9"),
        "anchors": part("UWB anchors (2)", C["anchors"].shape, "#7C3AED"),
        "tiller": part("Tiller head, beacon, stop and anchor", S("tiller", "beacon", "estop_head", "anchor_head"), "#1F2937"),
    }


ORDER = ["subframe", "stops", "cam", "jaw", "motors", "arms", "pin", "springs", "lever", "enc", "inside", "lid",
         "hoop", "edge", "lidar", "anchors", "tiller"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    tx, tz = D["handle_top"]
    off = {"subframe": (0, 0, 0), "stops": (-170, 0, -40), "cam": (-60, 0, -170), "jaw": (-480, 0, 250),
           "motors": (0, 0, -500), "arms": (0, 0, -290), "pin": (230, 0, -250), "springs": (-150, 0, -330),
           "lever": (0, -400, 220), "enc": (0, 0, 260), "inside": (0, 0, 420), "lid": (0, 0, 600),
           "hoop": (600, 0, 60), "edge": (820, 0, 60), "lidar": (620, 0, 300), "anchors": (800, 0, 260),
           "tiller": (430 - tx + 700, 0, -tz + 900)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "PalletPilot prototype kit: every component, pulled apart",
                       subtitle="Numbered in build order. The donor jack is not shown. Seen from the handle end, left side and above",
                       elev=22, azim=-50, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(which=None):
    import build123d as b
    M = made()
    base = dict(project="PalletPilot", date=DATE)
    out = []
    Y = donor_yoke()

    def want(n):
        return which is None or str(n) in which

    if want(101):
        out.append(bv.component_sheet(
            Part("Subframe", C["subframe"].shape, COL["subframe"]), [Y, M["arms"], M["motors"], M["hoop"]],
            dwg_no="PLP-DWG-101", title="PalletPilot subframe (top plate and welded hangers): making sketch",
            material="Steel plate 5 mm, 6 mm and 10 mm, S275 or A36; welded",
            notes=["Top plate: 5 mm steel, 295 x 400 mm. Front corners cut off at 45 degrees,",
                   "  50 mm along each edge. Pump notch: radius 62 mm, centred 15 mm in",
                   "  front of the front edge on the centre line (reaches 47 mm in).",
                   "Holes (from the front edge; sideways from the centre line):",
                   "  clamp bolts 13 mm at 49 back, 35 and 80 each side;",
                   "  enclosure feet 9 mm at 80 and 270 back, 162 each side.",
                   "Under the plate, square to it, welded both sides:",
                   "  front hangers, 6 mm, 24 x 59, inner faces 174 out, centred 75 back,",
                   "    16 mm hole 37 below the plate;",
                   "  rear hangers, 10 mm, 28 x 94, inner faces 180 out, centred 275 back,",
                   "    20 mm hole 74 below the plate;",
                   "  bumper brackets, 6 mm, 40 x 119, flush with the side edges, 215 to",
                   "    255 back, two 9 mm holes 109 below the plate at 225 and 245 back.",
                   "On top, left edge: lever bracket, 6 mm, 60 x 60, inner face 194 out,",
                   "  250 to 310 back; 12 mm pivot hole 35 up at 290 back; stop tab",
                   "  15 x 21 x 12 on its outer face, 13 mm up, 255 to 270 back.",
                   "Check: hangers square to the plate; the two hanger holes of each pair",
                   "  line up (a 16 mm and a 20 mm bar slide through)."],
            inset_view=(25, -55), **base))

    if want(102):
        out.append(bv.component_sheet(
            Part("Lower jaw", C["jaw"].shape, COL["jaw"]), [Y, M["subframe"]],
            dwg_no="PLP-DWG-102", title="PalletPilot lower jaw and packing bar: making sketch",
            material="Steel plate 10 mm; steel flat bar 34 x 15 mm (to suit the yoke)", view_shape=C["jaw"].shape, inset_view=(-25, -50),
            notes=["Jaw: 10 mm steel, 71 x 190 mm.",
                   "Packing bar: 34 mm wide, 190 long, as thick as the jack's yoke plate less",
                   "  1 mm (14 mm for the 15 mm plate drawn). Measure the yoke first.",
                   "Weld the packing bar on top of the jaw along its back edge, ends flush.",
                   "Drill four 13 mm holes through both, 49 mm from the jaw's front edge,",
                   "  35 and 80 mm each side of the centre line (drill with the top",
                   "  plate clamped on, so the holes line up).",
                   "Fit: the jaw goes under the yoke plate's back edge, the packing bar",
                   "  behind it, 2 mm clear of the edge. Four M12 bolts from below, nuts on",
                   "  the top plate: the yoke plate is gripped between the jaw and the top",
                   "  plate, with no hole drilled in the jack.",
                   "Check: with the bolts snug the jaw sits flat under the yoke plate."],
            **base))

    if want(103):
        arm = C["arm_l"].shape
        out.append(bv.component_sheet(
            Part("Drive arm", arm, COL["arms"]), [Y, M["subframe"], M["motors"], M["pin"]],
            dwg_no="PLP-DWG-103", title="PalletPilot drive arm (make 2, a left and a right): making sketch",
            material="Steel plate 10 mm; spring tab steel plate 10 mm", inset_view=(15, -40),
            notes=["Make two, a mirror pair (the left arm is drawn). 10 mm steel plate:",
                   "  three hole centres in one plane, ends rounded to 18 mm radius,",
                   "  36 mm wide between them.",
                   "Pivot hole 20 mm at the back end.",
                   "Axle hole 20 mm, 110 mm ahead of the pivot and 45 mm lower.",
                   "  Check it against the hub motor's shaft and flats.",
                   "Front end centre 195 mm ahead of the pivot and 95 mm lower.",
                   "Spring tab: 10 mm plate 44 x 44, welded square to the arm's outer",
                   "  face at the front end, its top face 90 mm below the pivot centre",
                   "  and centred on the front end. The spring sits on it.",
                   "Fit: the pivot pin passes the back hole; the motor shaft passes the",
                   "  axle hole with a 5 mm spacer between wheel and arm and a nut outside.",
                   "Check: the two arms laid back to back have their holes in line."],
            **base))

    if want(104):
        out.append(bv.component_sheet(
            Part("Pivot tubes", C["pivot_pin"].shape, COL["pin"]), [Y, M["subframe"], M["arms"]],
            dwg_no="PLP-DWG-104", title="PalletPilot arm pivot tubes, spacers and bolts: making sketch",
            material="Steel tube 20 x 3.5 mm; steel tube 30 x 5 mm; M12 bolts", inset_view=(20, -35),
            notes=["Pivot tubes (make 2): 20 mm outside, 13 mm bore, 31 mm long. Deburr",
                   "  the bore. Grease the outside before fitting.",
                   "Spacers: two tubes 30 mm outside, 20 mm bore, 5 mm long.",
                   "Each side, from the middle: tube through the arm, spacer, rear hanger;",
                   "  an M12 bolt through the bore with a 30 mm washer and a nyloc nut",
                   "  outside the hanger. The two sides are mirror images; the middle is open.",
                   "The arms must turn freely on the tubes; the bolts clamp the hangers only.",
                   "Check: each arm swings by hand through its full travel."],
            **base))

    if want(105):
        out.append(bv.component_sheet(
            Part("Cam shaft", C["camshaft"].shape, COL["cam"]), [Y, M["subframe"], M["springs"], M["arms"]],
            dwg_no="PLP-DWG-105", title="PalletPilot cam shaft, cams and crank: making sketch",
            material="Bright steel bar 16 mm; steel plate 12 mm (cams); flat bar 24 x 10 mm (crank)", inset_view=(-20, -40),
            notes=["Shaft: 16 mm bright steel bar, 419 mm long.",
                   "Cams (make 2): discs 72 mm across, 12 mm thick, with a 16 mm bore",
                   "  whose centre is 22 mm from the disc centre (the cam's throw).",
                   "Crank: 10 mm flat bar 24 wide, 74 long, ends rounded; 16 mm bore at",
                   "  one end, a 10 mm pin 18 long welded at the other, 50 mm apart.",
                   "Slide the shaft through both front hangers, then slide on a cam each",
                   "  side (outer faces 198 mm from the centre line) and the crank on the",
                   "  long end (outer face 221 mm out).",
                   "With the cams' thick side straight down and the crank pin straight",
                   "  up, drill a 5 mm hole through each hub and the shaft; fit roll pins.",
                   "Check: the shaft turns freely; cams and crank do not slip on it."],
            **base))

    if want(106):
        sad = side(C["saddles"].shape, 1) + side(C["straps"].shape, 1)
        out.append(bv.component_sheet(
            Part("Saddle and straps", sad, COL["saddle"]), [Y, M["arms"], M["cam"], part("Springs", C["springs"].shape, COL["spring"])],
            dwg_no="PLP-DWG-106", title="PalletPilot spring saddle and lift straps (make 2 sets): making sketch",
            material="Steel plate 8 mm (saddle); steel strip 12 x 4 mm (straps)", inset_view=(15, -30),
            notes=["Saddle (make 2): 8 mm steel, 44 x 34 mm. Turn a 2 mm deep ring",
                   "  groove in its underside, 34 mm across, to locate the spring top.",
                   "Straps (make 4): 4 mm steel strip 12 mm wide, 79 mm long.",
                   "  Bottom end: a 6.5 mm hole 5 mm from the end (bolted to the tab).",
                   "  Top end: a 6.5 mm wide slot, 12 mm long, ending 4 mm from the end.",
                   "Fit: one strap each side of the spring, bolted M6 to the tab and,",
                   "  through its slot, to the saddle. The slot lets the spring squash",
                   "  when a wheel rides a bump; when the lever lifts the saddle, the",
                   "  top of the slot catches and the straps lift the arm and wheel.",
                   "With the wheels down the saddle bolt sits 4 mm below the slot top.",
                   "Check: the saddle slides up and down the slots without binding."],
            **base))

    if want(107):
        out.append(bv.component_sheet(
            Part("Release lever", C["lever"].shape, COL["lever"]), [Y, M["subframe"], M["enc"], part("Link", C["link"].shape, COL["link"])],
            dwg_no="PLP-DWG-107", title="PalletPilot release lever: making sketch",
            material="Steel tube 20 x 10 x 2 mm; flat bar 20 x 10 mm; steel tube 28 mm (grip)", inset_view=(20, -60),
            notes=["Main tube: 20 x 10 x 2 mm rectangular steel tube, 376 mm long, the",
                   "  front end closed by a 2 mm plate. Pivot boss: 20 x 10 mm flat bar,",
                   "  34 long, butt-welded to the back end; 12 mm pivot hole 10 mm from",
                   "  its back end (410 mm overall).",
                   "Up-arm: 20 x 10 mm bar, ends rounded, welded at the pivot end standing",
                   "  square to the main bar; 10 mm hole 50 mm above the pivot hole.",
                   "Grip: 28 mm tube 30 mm long, welded across the front end so it",
                   "  stands out to the left, away from the enclosure.",
                   "Fit: on the bracket's pivot pin with an 11 mm spacer between the",
                   "  lever and the bracket. Wheels down: the lever lies forward,",
                   "  resting on the stop tab. Wheels up: the lever stands straight up.",
                   "The link joins the up-arm to the crank pin.",
                   "Check: the lever swings a quarter turn without touching anything."],
            **base))

    if want(108):
        out.append(bv.component_sheet(
            Part("Release link", C["link"].shape, COL["link"]), [Y, M["subframe"], M["cam"], part("Lever", C["lever"].shape, COL["lever"])],
            dwg_no="PLP-DWG-108", title="PalletPilot release link: making sketch",
            material="Steel flat bar 20 x 8 mm", inset_view=(20, -60),
            notes=["8 mm flat bar 20 mm wide, ends rounded to 10 mm radius.",
                   f"Two 10 mm holes {math.hypot(P['lever_pivot_xz'][0]-P['cam_xz'][0], P['lever_pivot_xz'][1]-P['cam_xz'][1]):.1f} mm apart between centres:",
                   "  exactly the distance from the cam shaft centre to the lever pivot,",
                   "  so the crank and the lever's up-arm stay parallel as they turn.",
                   "Fit: outboard of the crank and the lever, on their 10 mm pins, with",
                   "  a washer and split pin at each end.",
                   "Check: measure the cam shaft to lever pivot distance on the built",
                   "  subframe and match the link to it within 0.5 mm."],
            **base))

    if want(109):
        enc = S("enclosure", "feet", "lid")
        out.append(bv.component_sheet(
            Part("Enclosure", enc, COL["enc"]), [Y, M["subframe"], M["lever"]],
            dwg_no="PLP-DWG-109", title="PalletPilot enclosure, lid and feet: making sketch",
            material="Aluminium sheet 2 mm, 5052; aluminium angle 25 x 20 x 3 mm (feet)", inset_view=(25, -55),
            notes=["Box: 2 mm aluminium folded to 270 long x 300 wide x 90 tall, open",
                   "  top, corners riveted or welded; gasket on the top flange (IP54).",
                   "Lid: 2 mm aluminium, 270 x 300 with a 6 mm down-turned edge; held by",
                   "  six M5 screws into rivet nuts in the box flange.",
                   "Holes: right side, 40 mm for the disconnect, 180 from the front, 45",
                   "  up; rear face, 22 mm for the emergency stop, 80 left of centre,",
                   "  45 up; cable glands as the wiring needs, never in the lid.",
                   "Feet (make 4): 25 x 20 x 3 angle, 24 long; 9 mm hole in the flat leg",
                   "  12 from the box side. Rivet the upright leg to the box side with two",
                   "  4.8 mm rivets, 20 and 210 mm from the front, bottoms flush.",
                   "Fit: the box stands on the top plate; one M8 bolt through each foot.",
                   "Check: the lid top is no more than 320 mm above the floor when fitted."],
            **base))

    if want(110):
        out.append(bv.component_sheet(
            Part("Bumper hoop", C["hoop"].shape, COL["hoop"]), [Y, M["subframe"], M["motors"]],
            dwg_no="PLP-DWG-110", title="PalletPilot bumper hoop: making sketch",
            material="Steel rectangular tube 40 x 20 x 2 mm", inset_view=(35, -40),
            notes=["A U of 40 x 20 x 2 tube, standing 40 tall, 20 deep.",
                   "Front bar 440 long outside; two side legs 210 long outside, mitred",
                   "  at 45 degrees to the front bar and welded all round.",
                   "Side legs: two 11 mm holes in the inner face of each, 120 and 140 mm",
                   "  from the leg's open end, centred on the tube's height; set an M8",
                   "  rivet nut in each.",
                   "Fit: the inner faces of the legs bear on the subframe's bumper",
                   "  brackets; two M8 bolts each side. The tube's bottom is 90 mm above",
                   "  the floor; the front bar is 30 mm behind the wheel treads.",
                   "The safety edge rail is riveted to the front and side faces.",
                   "Check: the legs are parallel, 400 mm apart inside, within 1 mm."],
            **base))

    if want(111):
        out.append(bv.component_sheet(
            Part("Scanner shelf", C["lidar_bracket"].shape, "#64748B"), [M["hoop"], part("Safety scanner", C["lidar"].shape, "#0EA5E9")],
            dwg_no="PLP-DWG-111", title="PalletPilot safety scanner shelf: making sketch",
            material="Steel plate 3 mm", inset_view=(25, -50),
            notes=["Shelf: one flat piece of 3 mm steel plate, 118 long x 80 wide,",
                   "  laser or plasma cut. No bending.",
                   "Holes: two 5.5 mm holes, 30 apart sideways, 68 from the back edge,",
                   "  to match the rivet nuts in the top of the hoop's front bar; four",
                   "  more to suit the scanner's own mounting holes.",
                   "Fit: the shelf lies on the top of the hoop's front bar, reaching 58 mm",
                   "  back and 40 mm forward, with 2 mm of air over the safety edge. The",
                   "  scanner stands on it: scan plane 173 mm above the floor, front 10 mm",
                   "  behind the safety edge face.",
                   "Check: shelf flat and level within 1 degree; 2 mm clear of the edge."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(which=None):
    out = []
    px, pz = P["pivot_xz"]
    cx, cz = P["cam_xz"]

    def want(n):
        return which is None or str(n) in which

    def j(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    if want(1):
        bx = (105, 215, P["clamp_bolt_y"][1], 125, 172, 245)
        yoke_plate = C["donor_yoke"].shape & box(50, 170, -120, 120, P["yoke_z0"], P["yoke_top"])
        j(1, [part("Jack's yoke plate (donor)", win(yoke_plate, *bx), "#A8A29E"),
              part("Top plate", win(C["subframe"].shape, *bx), COL["subframe"]),
              part("Lower jaw and packing bar", win(C["jaw"].shape, *bx), COL["jaw"]),
              part("M12 bolt, nut on top", win(C["clamp_bolts"].shape, *bx), COL["bolt"])],
          "the clamp on the jack's yoke plate (cut through a bolt)",
          "Seen from the left side. The yoke plate is squeezed between the top plate and the jaw; the bolt passes behind its edge",
          elev=0.5, azim=-90, size=(8, 6))
    if want(2):
        bx = (360, 440, 150, 200, 110, 218)
        j(2, [part("Rear hanger", win(C["subframe"].shape, *bx), COL["subframe"]),
              part("Drive arm", win(C["arm_r"].shape, *bx), COL["arms"]),
              part("Pivot tube, spacer and nut", win(C["pivot_pin"].shape, *bx), COL["pin"])],
          "drive arm on its pivot tube (right side, rear)",
          "Spacer between arm and hanger; the bolt and nut clamp the hanger, the arm turns on the tube",
          elev=12, azim=-55, size=(8, 6))
    if want(3):
        bx = (240, 340, 135, 190, 30, 100)
        j(3, [part("Hub motor (cut through its shaft)", win(C["motors"].shape, 240, 340, 135, 160, 30, 100), "#374151"),
              part("Shaft, 5 mm spacer and nut", win(C["motors"].shape, 240, 340, 160, 190, 30, 100), "#B45309"),
              part("Drive arm", win(C["arm_r"].shape, *bx), COL["arms"])],
          "hub motor shaft in the drive arm (right side, cut through the shaft)",
          "Seen from above. Shaft through the arm's axle hole, 5 mm spacer on the inside, nut on the outside",
          elev=89, azim=-90, size=(8, 6))
    if want(4):
        bx = (160, 250, 160, 225, 40, 205)
        j(4, [part("Front hanger", win(C["subframe"].shape, *bx), COL["subframe"]),
              part("Cam", win(C["camshaft"].shape, *bx), COL["cam"]),
              part("Saddle", win(C["saddles"].shape, *bx), COL["saddle"]),
              part("Preload spring", win(C["springs"].shape, *bx), COL["spring"]),
              part("Lift straps", win(C["straps"].shape, *bx), COL["strap"]),
              part("Spring tab on the arm", win(C["arm_r"].shape, *bx), COL["arms"])],
          "spring, saddle and cam (right side, front)",
          "Seen from outside. The cam presses the saddle onto the spring; the spring presses the arm, so the wheel, down",
          elev=10, azim=60, size=(8, 6))
    if want(5):
        bx = (150, 450, -260, -185, 160, 335)
        j(5, [part("Crank on the cam shaft", win(C["camshaft"].shape, *bx), COL["cam"]),
              part("Release link", win(C["link"].shape, *bx), COL["link"]),
              part("Release lever", win(C["lever"].shape, *bx), COL["lever"]),
              part("Pins and spacer", win(C["lever_pins"].shape, *bx), COL["bolt"]),
              part("Lever bracket and stop", win(C["subframe"].shape, *bx), COL["subframe"])],
          "lever, link and crank (left side), wheels down",
          "Crank and lever up-arm stay parallel; the lever rests on its stop",
          elev=8, azim=-95, size=(9, 6))
    if want(6):
        R = release_state(C)
        fixed = (C["subframe"].shape & box(-100, 600, -400, 400, 0, P["plate_z"] - 0.5)) + S("pivot_pin", "hoop")
        moved = [part("Release lever (raised)", R["lever"], COL["lever"]), part("Link", R["link"], COL["link"]),
                 part("Cam shaft (turned a quarter)", R["camshaft"], COL["cam"]),
                 part("Saddles (raised 22 mm)", R["saddles"], COL["saddle"]),
                 part("Drive arms (lifted)", R["arm_r"] + R["arm_l"], COL["arms"]),
                 part("Hub motors, 10 mm clear of the floor", R["motors"], "#374151")]
        j(6, moved + [part("Hangers, brackets and hoop (fixed; top plate not shown)", fixed, COL["donor"])],
          "the release with the lever raised",
          "Raise the lever: the cams turn, the saddles rise, the straps lift the arms; the drive wheels clear the floor",
          elev=10, azim=-110, size=(9, 6))
    if want(7):
        bx = (330, 395, 180, 225, 85, 225)
        j(7, [part("Bumper bracket on the subframe", win(C["subframe"].shape, *bx), COL["subframe"]),
              part("Hoop side leg", win(C["hoop"].shape, *bx), COL["hoop"]),
              part("M8 bolts into rivet nuts", win(C["hoop_bolts"].shape, *bx), COL["bolt"]),
              part("Side safety edge", win(C["edge"].shape, *bx), COL["edge"])],
          "bumper hoop on the subframe bracket (right side)",
          "Seen from inside. Two M8 bolts through the bracket into rivet nuts in the tube",
          elev=15, azim=-70, size=(8, 6))
    if want(8):
        bx = (180, 230, 130, 185, 205, 260)
        j(8, [part("Top plate", win(C["subframe"].shape, *bx), COL["subframe"]),
              part("Enclosure side", win(C["enclosure"].shape, *bx), COL["enc"]),
              part("Foot, riveted to the side", win(C["feet"].shape, *bx), "#94A3B8"),
              part("M8 bolt and nut", win(C["feet_bolts"].shape, *bx), COL["bolt"])],
          "enclosure foot on the top plate (right front)",
          "Seen from outside. Each foot is riveted to the box side and bolted through the top plate",
          elev=25, azim=40, size=(8, 6))
    if want(9):
        bx = (400, 500, -250, 60, 80, 230)
        j(9, [part("Hoop front bar", win(C["hoop"].shape, *bx), COL["hoop"]),
              part("Front safety edge", win(C["edge"].shape, *bx), COL["edge"]),
              part("Scanner shelf", win(C["lidar_bracket"].shape, *bx), "#64748B"),
              part("Safety scanner", win(C["lidar"].shape, *bx), "#0EA5E9"),
              part("UWB anchor on its corner plate", win(C["anchors"].shape, *bx), "#7C3AED")],
          "safety scanner and anchor on the hoop (left half)",
          "Seen from behind the hoop. Scanner scan plane 173 mm up, its front 10 mm behind the edge face; the anchor stays below it",
          elev=25, azim=-150, size=(8, 6))
    if want(10):
        from build123d import Pos, Rot
        kx = P["kingpin_x"]
        T = Pos(kx, 0, 0) * Rot(0, 0, P["steer_stop_deg"]) * Pos(-kx, 0, 0)
        kit = [part("Steering stop (rubber, shown red)", T * C["steer_stops"].shape, "#DC2626"),
               part("Top plate", T * (C["subframe"].shape & box(-100, 600, -400, 400, P["plate_z"] - 0.5, 400)), COL["subframe"]),
               part("Jack frame head (does not steer)", C["donor_fixed"].shape & box(-120, 20, -360, 360, 0, 260), COL["donor"])]
        j(10, kit, f"steering stop at {P['steer_stop_deg']:.0f} degrees (seen from below)",
          "Handle turned fully: the rubber stop under the top plate's corner meets the jack's frame head first",
          elev=-55, azim=-40, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    M = made()
    out = []
    Y = donor_yoke()

    def want(n):
        return which is None or str(n) in which

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e, name=None):
        return Part(name or p.name, p.shape, p.color, None, tuple(e), p.alpha)

    sub_ = M["subframe"]
    st(1, [sub_], [mv(M["stops"], (0, 0, -90))], "steering stops under the top plate",
       "Plate upside down on the bench: each stop on two M8 bolts under a front corner", elev=-35, azim=-60)
    st(2, [sub_, M["stops"]], [mv(M["cam"], (0, -300, 0), "Cam shaft, then cams and crank")],
       "cam shaft through the front hangers", "Slide the shaft in from the left; cams and crank on, roll pins in",
       elev=-25, azim=-70)
    base = [sub_, M["stops"], M["cam"]]
    st(3, [Y], [mv(part("Subframe with stops and cam shaft", S("subframe", "steer_stops", "camshaft"), COL["subframe"]), (320, 0, 0))],
       "subframe onto the jack's yoke", "Slide it forward over the yoke plate until the pump sits in the notch",
       elev=22, azim=-55)
    st(4, [Y] + base, [mv(M["jaw"], (0, 0, -120))], "lower jaw under the yoke plate",
       "Four M12 bolts from below, nuts on top; tighten evenly to 80 N·m", elev=-20, azim=-60, label_done=False)
    on_jack = [Y] + base + [M["jaw"]]
    st(5, [M["arms"]], [mv(M["motors"], (0, 0, -160))], "hub motors into the drive arms (on the bench)",
       "Shaft through the axle hole with the 5 mm spacer inside; nut outside, motor maker's torque", elev=20, azim=-40)
    st(6, on_jack, [mv(part("Arms with motors", S("arm_r", "arm_l", "motors"), COL["arms"]), (0, 0, -150)),
                    mv(M["pin"], (0, -320, 0))],
       "arms and motors onto the pivot tubes", "Lift the arms under the rear hangers; push a pivot tube through each arm and hanger with its spacer; bolt",
       elev=15, azim=-55, label_done=False)
    drive = on_jack + [M["arms"], M["motors"], M["pin"]]
    spr = S("springs", "saddles", "straps")
    st(7, drive, [part("Left spring, saddle and straps", side(spr, -1), COL["spring"], (0, -130, -60)),
                  part("Right spring, saddle and straps", side(spr, 1), COL["spring"], (280, 0, -90))],
       "springs, saddles and lift straps",
       "Turn the crank toward the back first (cams up), place each spring and saddle, bolt the straps, turn back",
       elev=10, azim=-60, label_done=False)
    st(8, drive + [M["springs"]], [mv(M["lever"], (0, -60, 220))], "release lever and link",
       "Lever on its pivot pin with the spacer; link onto the crank pin and the up-arm; washers and split pins",
       elev=15, azim=-70, label_done=False)
    full_drive = drive + [M["springs"], M["lever"]]
    st(9, full_drive, [mv(M["enc"], (0, 0, 200))], "enclosure onto the top plate",
       "Four M8 bolts through the feet and the top plate, nuts below", elev=22, azim=-55, label_done=False)
    st(10, [M["enc"]], [mv(M["inside"], (0, 0, 160))], "pack, driver, contactors and controller into the enclosure",
       "Fit and wire as the wiring diagram shows, with the disconnect off and the pack fuse out", elev=40, azim=-55)
    boxed = full_drive + [M["enc"], M["inside"]]
    st(11, boxed, [mv(M["lid"], (0, 0, 150))], "close the lid", "Gasket clean, no wire across it; six M5 screws",
       elev=22, azim=-55, label_done=False)
    closed = boxed + [M["lid"]]
    st(12, closed, [mv(M["hoop"], (250, 0, 0))], "bumper hoop onto the brackets",
       "Slide the hoop forward over the brackets; two M8 bolts each side into the rivet nuts", elev=20, azim=-40, label_done=False)
    st(13, closed + [M["hoop"]], [mv(M["edge"], (220, 0, 0))], "safety edge onto the hoop",
       "Rivet the edge's rail to the front and side faces; run its lead to the evaluation unit", elev=20, azim=-40, label_done=False)
    st(14, closed + [M["hoop"], M["edge"]], [mv(M["lidar"], (0, 0, 120)), mv(M["anchors"], (0, 0, 90))],
       "safety scanner and corner anchors onto the hoop", "M5 screws into rivet nuts; scanner scan plane 173 mm above the floor",
       elev=25, azim=-40, label_done=False)
    tx, tz = D["handle_top"]
    hand = part("Jack handle (donor)", C["donor_yoke"].shape & box(tx - 260, tx + 200, -200, 200, tz - 420, tz + 200), COL["donor"])
    st(15, [hand], [mv(M["tiller"], (60, 0, 160))], "tiller head onto the handle",
       "Remove the jack's grip; clamp the head on the handle tube; spiral-wrapped cable down the handle",
       elev=15, azim=-60, label_done=True)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "PalletPilot prototype: block-level power and stop-chain wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; crimped lugs or ferrules on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/palletpilot", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, ORG = "#B91C1C", "#1D4ED8", "#6B7280", "#C2410C"
    # power path, top row
    blk(2, 46, 13, 12, "LiFePO4 pack", "25.6 V, 20 Ah,\nBMS 50 A", "#D4A017")
    blk(19, 46, 11, 12, "Main fuse", "80 A, at the\npack terminal", "#991B1B")
    blk(34, 46, 12, 12, "Disconnect", "lockable,\nright side", "#991B1B")
    blk(50, 46, 14, 12, "Contactor K1", "24 V coil,\nrelay channel A", "#991B1B")
    blk(68, 46, 14, 12, "Contactor K2", "24 V coil,\nrelay channel B", "#991B1B")
    blk(86, 46, 14, 12, "Motor driver", "2 x 15 A, CAN,\nbrake outputs", "#B45309")
    blk(104, 46, 14, 12, "Hub motors", "2 x 24 V with\nspring brakes", "#111827")
    wire([(15, 52), (19, 52)], RED); wire([(30, 52), (34, 52)], RED); wire([(46, 52), (50, 52)], RED)
    wire([(64, 52), (68, 52)], RED); wire([(82, 52), (86, 52)], RED); wire([(100, 52), (104, 52)], RED)
    lab(17, 59.5, "all main power 5.3 mm² (10 AWG)", RED)
    lab(66, 44.2, "pre-charge resistor\nacross K2 (driver bus)", RED, "center")
    # control row
    blk(2, 22, 15, 14, "Emergency stops", "tiller head and\nenclosure rear,\n2 NC contacts each", "#DC2626")
    blk(21, 22, 15, 14, "Safety edge", "evaluation unit,\nfront and sides", "#1F2937")
    blk(42, 20, 18, 16, "Safety relay", "dual channel;\nopens K1 and K2;\nmanual reset", "#15803D")
    blk(66, 20, 16, 16, "Controller", "ESP32-S3 class,\nCAN, SPI;\nasks for a stop,\nnever closes the chain", "#15803D")
    blk(88, 22, 14, 14, "UWB anchors", "3 modules on SPI;\ntag with stop\nbutton (radio)", "#7C3AED")
    blk(105, 20, 13, 16, "Safety scanner", "24 V, fused;\nsafety outputs\nto the relay;\nfields stored\nin the scanner", "#0EA5E9")
    wire([(17, 31), (42, 31)], ORG); lab(3, 19.6, "stop channel A and B, 0.75 mm²", ORG)
    wire([(28.5, 36), (28.5, 39), (51, 39), (51, 36)], ORG); lab(30, 40.7, "edge output to relay inputs", ORG)
    wire([(54, 36), (54, 46)], ORG, 1.4); wire([(57, 36), (57, 42), (75, 42), (75, 46)], ORG, 1.4)
    lab(57.6, 40.7, "coil A and coil B, 0.75 mm²", ORG)
    wire([(60, 28), (66, 28)], GRY, 1.2); lab(61, 26.2, "stop request", GRY)
    wire([(82, 29), (88, 29)], BLU, 1.2)
    wire([(111.5, 20), (111.5, 18.3), (46, 18.3), (46, 20)], ORG, 1.4); lab(84, 17.2, "scanner safety outputs to relay inputs", ORG)
    wire([(74, 36), (74, 40.5), (93, 40.5), (93, 46)], BLU, 1.2); lab(80, 38.6, "CAN, twisted pair", BLU)
    blk(66, 6, 16, 9, "DC-DC 24 V to 5 V", "controller and\nanchors (fused 3 A)", "#16A34A")
    wire([(74, 15), (74, 20)], RED, 1.2); lab(74.6, 16.0, "1 mm²", RED)
    ax.text(2, 13, "Safety: disconnect off and pack fuse out until the stop points of section 6 are passed.", fontsize=7.6,
            color="#B45309", fontweight="bold")
    ax.text(2, 10, "The hardwired stops and the edge open both contactors through the relay;", fontsize=7.2, color=MUT)
    ax.text(2, 7.6, "software can only request a stop. The brakes close when power is removed.", fontsize=7.2, color=MUT)
    ax.text(2, 5.2, "Red: power. Orange: stop chain. Blue: data. Grey: controller requests. 25.6 V nominal, extra-low voltage.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    what, sel = args[0], args[1:]
    if what in fns and sel and what in ("sheets", "joints", "steps"):
        print(what, sel, "->", fns[what](set(sel)))
    else:
        for w in args:
            print(w, "->", fns[w]())
