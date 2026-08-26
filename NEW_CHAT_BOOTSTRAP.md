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
- Normal private build promotion is now GitHub Actions → VPS staging → `spatialforge` runtime-owner promotion on service restart. Do not widen deploy-user access to private build files.
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

A small supported 11-target generic face profile was then applied and proven through the full runtime chain:
- targets apply/bake successfully
- rig preserved
- GLB export succeeds
- fresh import succeeds
- final face workflow run `32934697014` PASS
- artifact `9594484821`
- private VPS build ID: `generic-face-quality-v1`
- private install run `32938078210` PASS
- Creator opened `generic-face-quality-v1` from the authenticated Asset Library on Android and confirmed it renders in the web viewer.

**Important visual verdict:** the Creator inspected the actual web model and correctly judged that it looks almost the same as the baseline. The first 11-target pass proves controllability and delivery, not meaningful visual quality improvement. Do not call P3Q.3 complete yet.

The current temporary/blocky hair also covers much of the face and makes comparison worse.

### ACTIVE NEXT — P3Q.3B Visible Face Sculpt Pass

Continue here immediately in a new chat.

Required next actions:
1. Read `IMPLEMENTATION_PLAN.md`, `ROADMAP.md`, this file, and `skills/spatial-forge-3d/SKILL.md` before editing code.
2. Temporarily remove/disable the current hair asset for face-review builds only. Do not delete the hair pathway permanently; this is an inspection aid.
3. Keep existing body macro/phenotype controls locked so body proportions do not drift while sculpting the face.
4. Use a stronger but still human-looking subset of already-proven MPFB face targets. Prioritize readable head/jaw/chin/cheek/nose/eye-region/lip form.
5. Tighten the portrait camera so head/shoulders dominate the evidence image.
6. Build/export/fresh-import as usual.
7. Produce fixed baseline-vs-revised evidence and inspect it visually before deployment.
8. Only if the facial change is clearly visible and not malformed, install it as a new private VPS build and tell the Creator to inspect it in `forge.drthorne.uk`.
9. Do not add production skin, eyes, brows, or hair materials yet. First prove readable facial geometry. Those belong to P3Q.4/P3Q.5.

### Quality order after P3Q.3B

Current evidence-driven order:
- P3Q.3B visible face form — ACTIVE
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
- The Asset Library currently contains the original `p3-private-proof` and the newer `generic-face-quality-v1` private build.
- New private build installation uses `control-plane/staged_install.py`: Actions places four allowed assets plus `install.json` into `/srv/ianeo-spatial-forge/app/build-staging/current`; service restart lets the `spatialforge` runtime owner promote the staged build into private storage. This avoided adding broad sudo/private-file permissions to `eidolon-deploy`.
- Do not fall back to public Pages demo paths as the normal inspection workflow. User-visible quality builds should be installed into the private Asset Library when ready for review.

## Working Rules

- `IMPLEMENTATION_PLAN.md` is the canonical checkbox state.
- Structural PASS and visual PASS are separate gates.
- A green workflow, successful target application, valid GLB, rig counts, or web rendering does not prove visual improvement.
- Inspect fixed visual evidence before claiming quality improvement.
- Do not invent unsupported controls; use actual MPFB runtime target inventory.
- Keep changes small, reproducible, and simple; avoid over-engineering.
- No paid dependency without explicit Creator approval.
- Keep private/canonical assets out of this public repo.
- Sync `IMPLEMENTATION_PLAN.md`, `ROADMAP.md`, and `NEW_CHAT_BOOTSTRAP.md` after every completed slice or material status change.
