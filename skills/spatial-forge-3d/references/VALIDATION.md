# Spatial Forge Validation

Use this reference whenever a slice makes structural, export, rigging, revision-preservation, or visual-quality claims.

## Two independent gates

### Structural gate

Use cheap deterministic inspection for claims such as:

- output files exist and are non-empty
- Blender completes headlessly
- GLB parses
- expected mesh/skin/joint structures exist
- transforms and scale are plausible
- expected metadata is present
- fresh import succeeds
- locked manifest fields remain unchanged

Structural PASS does not imply visual PASS.

### Visual gate

Use fixed comparable previews for claims such as:

- human proportions look plausible
- intended body change is visible
- unrelated visual identity did not drift
- camera/composition works
- materials read correctly
- scene placement matches the request

Automated scores may assist but never replace visual inspection for these claims.

## Character evidence defaults

Early generic character proof:

- front view
- three-quarter view

For identity-sensitive or scoped revision work, prefer a fixed evidence set with the same:

- pose
- camera transform
- focal length
- subject distance/framing
- lighting
- background
- output dimensions

Add side/back views only when they materially test the claim.

## GLB validation

When GLB is a deliverable:

1. confirm export completed
2. parse the GLB/container
3. inspect expected structural elements
4. fresh-import into a clean scene when practical
5. render or inspect the imported artifact if appearance/deformation matters

The exported artifact is what downstream clients receive; validation must not stop at the authored `.blend` scene.

## Rig validation

For a static rigged-character slice, prove at minimum:

- skin exists
- joints/bones exist
- expected rig survives GLB export

Do not add animation/deformation test suites until a slice actually depends on motion quality.

## Revision validation

For V1 → V2:

- list explicitly requested changed fields
- list inherited locked fields
- compare manifest values
- compare result metadata
- render with comparable evidence settings
- inspect intended change and unintended drift separately

If a visual lock cannot be guaranteed by numeric manifest equality alone, say so. Numeric sameness is evidence, not proof of perceived identity.

## Failure handling

When a workflow fails:

`run → job → failed step → log → concrete root cause → smallest repair → rerun`

Do not add unrelated guards before the actual failure mode is understood.

## Cost discipline

Keep evidence proportional to the claim. Prefer low-cost EEVEE/workbench-style previews and structural inspection over high-quality final renders during engineering proof slices.
