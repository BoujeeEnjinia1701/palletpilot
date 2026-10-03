"""PalletPilot concept media (TRL 3), built from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; key figures and flow values come from
PLP-CAL-001 (docs/04-calcs/sizing.py). Donor parts are grey and carry no BOM number;
kit parts are colored and numbered to match bom/bom.csv. CONCEPT, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from concept import Part, render_all  # noqa: E402
from model import build_parts, box  # noqa: E402

src = build_parts()
parts = [Part(name, shape, color, bom, explode) for name, shape, color, bom, explode in
         sorted(src.values(), key=lambda v: -1 if v[3] is None and v[0].startswith("Donor") else (v[3] or 99))]
for _p in parts:                    # pull the two far-right exploded parts in so their callouts stay off the image edge
    if _p.bom in (9, 18):
        _p.explode = (_p.explode[0] - 110, _p.explode[1], _p.explode[2])

# Context for the hero render only: a 48 x 40 in stringer pallet with cartons over the forks
PX0, PX1 = -1225.0, -5.0
pallet = (box(PX0, PX1, -508, 508, 118, 140)
          + box(PX0, PX1, -508, -470, 0, 118) + box(PX0, PX1, -19, 19, 0, 118) + box(PX0, PX1, 470, 508, 0, 118))
cartons = box(PX0 + 20, PX1 - 20, -490, 490, 140, 700)
context = [Part("Pallet", pallet, "#C8A97E"), Part("Cartons, about 1,000 kg", cartons, "#D6C3A0")]

render_all(
    parts, project="PalletPilot", title="Pallet jack retrofit concept", dwg_no="PLP-DWG-010",
    date="2026-10-02", rev="P3",
    key_figures=["Design load 1,000 kg; 1,500 kg on level floors at 0.8 m/s",
                 "Walk up to 1.2 m/s; follow up to 0.6 m/s",
                 "Layered stopping: safety scanner field 0.80 m, bumper last",
                 "Scanner stop from 0.6 m/s: 0.36 m level (PLP-CAL-001)",
                 "Pack 512 Wh: shift uses 310 of 410 Wh usable",
                 "Kit about 42.9 kg; about $5,065 in parts (target $1,610)"],
    context=context,
    cut_exclude=("Contact bumper (hoop and safety edge)", "UWB anchors (3)", "Manual release: cam shaft, lever, springs", "Steering stops"),
    flow={"title": "energy per 8 h shift, 60 pallet moves (estimates, PLP-CAL-001)", "unit": "Wh",
          "stages": [("Wall outlet (AC)", 370), ("Pack, delivered", 310), ("Motor driver input", 219),
                     ("Work at the wheels", 153)],
          "losses": [(0, "Charging (est.)", 61), (1, "Controls and scanner (est.)", 90),
                     (2, "Motors (est.)", 66)]},
)
for d in (ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
print("media refreshed")
