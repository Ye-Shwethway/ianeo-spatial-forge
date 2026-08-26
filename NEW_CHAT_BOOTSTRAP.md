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

### Active Next Slice — P3Q.3 Face Control

Face work moves ahead of P3Q.2 because the inspected baseline shows it offers the largest visible gain.

Next tasks:
1. Inspect MPFB `2.0.17` for real programmatic face/head target controls; do not invent schema fields.
2. Select a small high-value supported set for head, jaw/chin, nose, eyes, brows, and mouth/lips where available.
3. Add a tighter fixed portrait evidence view.
4. Build a generic face revision while locking existing body macro controls.
5. Compare baseline vs revision visually and verify GLB/fresh import.

P3Q.2 mesh/surface polish remains required after the face-control proof.

## Remaining Quality Ladder

- [ ] P3Q.2 mesh/surface polish
- [ ] P3Q.3 face control — ACTIVE
- [ ] P3Q.4 PBR skin/eyes/mouth
- [ ] P3Q.5 hair/brows/facial hair
- [ ] P3Q.6 clothing
- [ ] P3Q.7 deformation/pose quality
- [ ] P3Q.8 presentation defaults
- [ ] P3Q.9 final generic quality proof against P3Q.1.

## Working Rules

- Use `IMPLEMENTATION_PLAN.md` as canonical checkbox state.
- Read `skills/spatial-forge-3d/SKILL.md` for 3D work.
- Keep changes small and reproducible; avoid over-engineering.
- Never fake unsupported precision/control.
- Structural PASS and visual PASS are separate gates.
- Inspect fixed visual evidence before claiming quality improvement.
- Sync docs after each completed slice.
