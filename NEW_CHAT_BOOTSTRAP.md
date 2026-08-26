# IANEO Spatial Forge — New Chat Bootstrap

## Canonical Repository

`Ye-Shwethway/ianeo-spatial-forge`

## Mission

Build a zero-incremental-cost, phone-first, agent-operated 3D creation pipeline where the Creator interacts through IANEO rather than manually operating Blender.

## Current Architecture

- Public repo: engine code, workflows, schemas, skills, viewer/Pages Function code, and generic fixtures only.
- Private generated/canonical assets stay outside the public repo.
- Proven stack: Blender `4.5.12 LTS` + MPFB `2.0.17`.
- Blender builds run in GitHub Actions; VPS is private storage/control, not a render machine.
- Primary web surface: `https://forge.drthorne.uk/` behind Cloudflare Access Email OTP.
- Browser control is same-origin through `/api/*`; Pages Function forwards authenticated requests server-side to the protected VPS origin.
- Asset Library list/open/delete and protected 3D viewing are proven on Android.
- Normal private build promotion is GitHub Actions → VPS staging → `spatialforge` runtime-owner promotion on service restart. Do not widen deploy-user access to private build files.
- Bamboo/Termux/root are bootstrap/emergency-only.
- Telegram and MCP remain deferred while character visual quality is being proven.

## Proven Phases

- **P0 PASS:** headless Blender, run `32859113238`.
- **P1 PASS:** MPFB human + rig + GLB, run `32860562804`.
- **P2 PASS:** manifest controls, unsupported precision, scoped revision/locks; runs `32864360900`, `32864975879`, `32877860898`.
- **P2V PASS:** phone viewer and Pages deployment.
- **P3 PASS:** protected VPS control/assets, temporary sessions, automated deployment, Android private GLB retrieval, authenticated web Asset Library.

## Active Phase — P3Q Character Quality & Visual Fidelity

### P3Q.1 — PASS

Fixed quality-baseline workflow is implemented with generic v1 and four evidence views: front, three-quarter, profile, face/upper-body close view.

Runtime proof:
- Character Quality Baseline run `32932834097` PASS
- artifact `9593852812`
- digest `sha256:513f432ee25037b8bb0555f851bb3f2954e153a217f70137d894ae0b20b57737`
- Blender `4.5.12 LTS`, MPFB `2.0.17`
- GLB: 1 mesh, 1 skin, 53 joints
- fresh import: 2 mesh objects, 1 armature, 53 joints
- `.blend`, `.glb`, four PNG evidence views, build result and fresh-import result inspected.

Visual baseline findings:
- body silhouette is usable but generic
- face is the largest quality bottleneck: weak eyes/nose/lips/jaw/chin readability
- single pale material creates a clay/mannequin look
- production skin/eyes/brows/hair are absent
- hands/feet and profile torso/hip forms remain basic.

### P3Q.3A — Face-Control Technical Proof PASS, Visual PASS NOT ACHIEVED

Actual installed MPFB `2.0.17` target data was probed before schema expansion.

Probe result:
- 530 bundled MPFB targets discovered
- 270 are face/head-related
- categories include head, eyes, nose, mouth/lips, chin and other facial regions.

The first supported 11-target profile proved the complete technical/runtime path:
- final workflow run `32934697014` PASS
- artifact `9594484821`
- private build ID `generic-face-quality-v1`
- private install run `32938078210` PASS
- Creator opened it from the authenticated Android Asset Library.

**Visual verdict:** the Creator judged the visible change too subtle. This remains a technical proof only.

### P3Q.3B — Visible Face Sculpt: BUILD + PRIVATE INSTALL PASS; CREATOR REVIEW PENDING

**Continue here immediately in a new chat. Do not rebuild blindly first. Ask/inspect the Creator's live verdict on the already-installed build `generic-face-sculpt-v2`.**

What changed and what was proven:
- The blocky obstruction that looked like hair was not an explicitly added hair asset. `scripts/build_face_quality.py` had no real hair asset; the obstruction came from MPFB helper geometry hidden only by a MASK modifier.
- Physically stripping helpers **before** rig creation breaks MPFB `game_engine` rig construction because required topology groups become empty (`ZeroDivisionError`).
- Commit `830420e` moved helper cleanup after rig creation/binding. The helper MASK can then be physically applied while retaining the rig.
- Correct cleanup result: `Hide helpers` applied; vertices `19,158 → 13,380`; 53-joint rig preserved.
- Run `32974243141` proved the corrected cleanup/rig order but still used `face-quality-v1` because the workflow profile path had not yet been switched. Treat that run as cleanup proof only, not v2 face-sculpt proof.
- Commit `02fcfd5` switched `.github/workflows/character-face-quality.yml` to `fixtures/generic-face-sculpt-v2.json` and added exact v2 assertions.
- Actual v2 run `32974854289` PASS.
- Artifact `9609141774`; digest `sha256:252da42af00832f8a934085c28ecaa7d44df0fcb52a5c3a1881476e299f0c026`.
- Profile ID: `face-sculpt-v2`.
- 19 supported target operations cover head width/depth, cheek bones/volume, chin width/height/prominence, nose width/depth, eye scale/height, brow angle, mouth width, and upper/lower lip volume.
- Body phenotype remained locked: gender `1.0`, age `0.36`, muscle `0.72`, weight `0.48`, height `0.62`, proportions `0.58`.
- GLB structural result: 1 mesh / 1 skin / 53 joints.
- Fresh import: 2 mesh objects / 1 armature / 53 joints.
- Evidence files visually inspected by IANEO: `front.png`, `three-quarter.png`, `profile.png`, `face-close.png`.
- IANEO visual finding: helper slabs are gone, face is unobstructed, jaw/chin/cheek and side-profile form are more readable, and no malformed mesh/body drift was observed. The white-clay material still makes eyes/brows/lips visually weak; do not confuse that material limitation with helper cleanup failure.
- Commit `ceaeada` updated the existing private installer to install this exact proven artifact as build ID `generic-face-sculpt-v2`.
- Private install run `32975345268` PASS: artifact download, exact payload verification, SSH staging, service promotion, installed-build verification, and staging cleanup all succeeded.

### Immediate next action

1. Creator opens `https://forge.drthorne.uk/` on Android.
2. In Asset Library choose **`generic-face-sculpt-v2` → Open 3D**.
3. Inspect front/side/rotated face at useful zoom and compare mentally/visually with `generic-face-quality-v1`.
4. If Creator says the facial form is clearly more useful and not malformed, mark P3Q.3B complete and move to P3Q.4 skin/eyes/mouth/lips.
5. If Creator still says it barely changes or dislikes the proportions, keep P3Q.3B open and revise from this v2 profile. Do not redo helper cleanup or control-plane work.
6. Do not add hair back yet during geometry verdict. Real hair/brows belong to P3Q.5; skin/eye/mouth appearance belongs to P3Q.4.

### Quality order after Creator verdict

Current evidence-driven order:
- Creator verdict on P3Q.3B visible face form — ACTIVE
- P3Q.4 GLB-safe skin/eyes/mouth/lips
- P3Q.5 hair/brows/facial hair
- P3Q.2 mesh/surface polish (still required, intentionally deferred)
- P3Q.6 clothing
- P3Q.7 deformation
- P3Q.8 presentation
- P3Q.9 final generic quality proof against baseline.

## Recent Control/Delivery Facts

- Web control path is canonical: `forge.drthorne.uk` → same-origin `/api/*` Pages Function → protected `assets.drthorne.uk` → VPS.
- All protected hostnames remain in the same Cloudflare Access application; eager redirect cookie is disabled.
- Browser does not authenticate directly to `assets.drthorne.uk` for normal control API use.
- Private review builds include the earlier `generic-face-quality-v1` and current `generic-face-sculpt-v2`; do not delete the v2 build before Creator review.
- New private build installation uses `control-plane/staged_install.py`: Actions places the four allowed web assets plus `install.json` into `/srv/ianeo-spatial-forge/app/build-staging/current`; service restart lets the `spatialforge` runtime owner promote the staged build into private storage.
- Do not fall back to public Pages demo paths as the normal inspection workflow. User-visible quality builds should be installed into the private Asset Library when ready for review.

## Working Rules

- `IMPLEMENTATION_PLAN.md` is the canonical checkbox state.
- Structural PASS and visual PASS are separate gates.
- A green workflow, successful target application, valid GLB, rig counts, or web rendering does not prove visual improvement.
- Inspect fixed visual evidence before claiming quality improvement, then require Creator live review for visual-slice closure.
- Do not invent unsupported controls; use actual MPFB runtime target inventory.
- Keep changes small, reproducible, and simple; avoid over-engineering.
- No paid dependency without explicit Creator approval.
- Keep private/canonical assets out of this public repo.
- Sync `IMPLEMENTATION_PLAN.md`, `ROADMAP.md`, and `NEW_CHAT_BOOTSTRAP.md` after every completed slice or material status change.
