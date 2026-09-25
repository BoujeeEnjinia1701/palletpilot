"""PalletPilot general arrangement sheet PLP-DWG-001, Rev P1 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/PLP-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(),
so they follow any parameter change. The concept sheet in media/ is PLP-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build, derived  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = build(with_donor=True)
    views = project_views(asm, work / "asm")
    bb = asm.bounding_box()
    s = Sheet(project="PalletPilot", title="General arrangement", dwg_no="PLP-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Kit on a 27 x 48 in donor jack (grey, reference); parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    # front view, from -Y: X to the right, floor at the bottom
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zf = Z(0)
    bf = D["bumper_face_x"]
    L += [ext(X(P["x_tip"]), zf + 1, X(P["x_tip"]), zf + 21), ext(X(bf), zf + 1, X(bf), zf + 21),
          ext(X(D["bare_rear_x"]), zf + 1, X(D["bare_rear_x"]), zf + 16)]
    L += dim_h(X(P["x_tip"]), X(bf), zf + 20, f"{D['overall_len']:,.0f} at floor level")
    L += dim_h(X(D["bare_rear_x"]), X(bf), zf + 15, f"{D['added_length']:.0f} added")
    L += [ext(X(P["kingpin_x"]), y - 2, X(P["kingpin_x"]), Z(P["pivot_z"])),
          ext(X(P["drive_x"]), y - 2, X(P["drive_x"]), Z(P["drive_r"]))]
    L += dim_h(X(P["kingpin_x"]), X(P["drive_x"]), y - 1, f"{D['trail']:.0f}")
    xr = X(bb.max.X)
    L += [ext(X(D['handle_top'][0]) + 8, Z(bb.max.Z), xr + 10, Z(bb.max.Z)),
          ext(X(bf) + 1, Z(P["pivot_z"]), xr + 5, Z(P["pivot_z"]))]
    L += dim_v(xr + 9, Z(bb.max.Z), zf, f"{bb.size.Z:,.0f}")
    L += dim_v(xr + 4, Z(P["pivot_z"]), zf, f"{P['pivot_z']:.0f} pivot")
    L.append(_t(X(P["kingpin_x"]), y - 5, "STEER AXIS TO DRIVE AXLE", 1.8, 400, MUTED, "middle"))
    # top view: Y up on the sheet
    x, y, w, h = c["top"]
    Yt = lambda my: y + (bb.max.Y - my) * k
    Xt = lambda mx: x + (mx - bb.min.X) * k
    L += dim_v(x - 4, Yt(P["out_w"] / 2), Yt(-P["out_w"] / 2), f"{P['out_w']:.0f}")
    L += [ext(Xt(bf), Yt(P["bumper_half_w"]), Xt(bf) + 9, Yt(P["bumper_half_w"])),
          ext(Xt(bf), Yt(-P["bumper_half_w"]), Xt(bf) + 9, Yt(-P["bumper_half_w"]))]
    L += dim_v(Xt(bf) + 8, Yt(P["bumper_half_w"]), Yt(-P["bumper_half_w"]), f"{2*P['bumper_half_w']:.0f}")
    # right view, from +X: Y to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += [ext(Yr(-P["anchor_y"]), Zr(P["anchor_top"]) , Yr(-P["anchor_y"]), y + h + 16),
          ext(Yr(P["anchor_y"]), Zr(P["anchor_top"]), Yr(P["anchor_y"]), y + h + 16)]
    L += dim_h(Yr(-P["anchor_y"]), Yr(P["anchor_y"]), y + h + 15, f"{D['anchor_baseline']:.0f} UWB")
    L += [ext(Yr(-P["drive_track"] / 2), Zr(0), Yr(-P["drive_track"] / 2), y + h + 21),
          ext(Yr(P["drive_track"] / 2), Zr(0), Yr(P["drive_track"] / 2), y + h + 21)]
    L += dim_h(Yr(-P["drive_track"] / 2), Yr(P["drive_track"] / 2), y + h + 20, f"{P['drive_track']:.0f} track")
    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 96, label="Isometric view (donor jack is reference)", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        "Front view from -Y; drive end (+X) leads in follow mode",
        f"Lidar scan plane {P['lidar_scan_z']:.0f} above floor; enclosure top {P['enc_top']:.0f}",
        f"Drive: two 200 mm hub motors, track {P['drive_track']:.0f}; axle {D['trail']:.0f} from steer axis to handle end",
        f"Preload 1.5 kN on the drive wheels (springs on the subframe)",
        f"Enclosure {P['enc_x1']-P['enc_x0']:.0f} x {2*P['enc_half_w']:.0f} x {P['enc_top']-P['enc_z0']:.0f}; top {P['enc_top']:.0f} under pivot {P['pivot_z']:.0f}",
        f"Handle clears enclosure: 40 at 70 deg, {D['handle_clear_90']:.0f} horizontal",
        f"Bumper face {D['added_length']:.0f} behind steer wheels; edge travel {P['edge_travel']:.0f}",
        "Lidar protective field 0.86 m ahead of the bumper (PLP-CAL-001)",
        f"UWB anchors {D['anchor_baseline']:.0f} apart at the bumper corners",
        "Kit about 41.7 kg (PLP-CAL-001); donor is reference only",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "PLP-DWG-001")
    txt = out.read_text()
    tag = _t(M + 6, M + 14, "PRELIMINARY, NOT FOR FABRICATION", 3.2, 600, "#B45309")
    if "PRELIMINARY" not in txt.split("MATERIAL")[0]:
        s._layers.append(tag)
        out = s.save(ROOT / "cad" / "drawings" / "PLP-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
