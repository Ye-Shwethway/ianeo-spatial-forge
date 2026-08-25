# Spatial Forge Creation Workflow

Use this reference for creating or substantially revising characters, props, or scenes.

## 1. Define the smallest build contract

Record only what the current slice must prove:

- asset/character identifier
- version
- intended use
- requested controllable properties
- locks inherited from the previous approved version
- engine/runtime versions
- required outputs
- required preview/evidence views
- known approximations or unsupported requests

Do not design future phases inside the current manifest.

## 2. Establish reference intent before detail

For visual work, separate:

- canonical/invariant facts
- current revision target
- scene-specific choices
- engine limitations

If reference images are available in a private future workflow, use them as visual evidence, not as permission to claim exact geometric recovery.

## 3. Build in readable stages

Prefer this order when applicable:

1. baseline / graybox
2. primary forms and scale
3. secondary forms
4. rig or deformation setup
5. materials/appearance
6. camera and lighting for evidence
7. export
8. validation

For MPFB character work, use the smallest proven scripted path. Do not manually reproduce functionality that MPFB already exposes reliably.

## 4. Keep source reproducible

Generation scripts should run from a clean headless Blender process with explicit inputs. Avoid hidden dependence on a previously edited `.blend` file unless a later canonical-asset phase intentionally introduces that dependency.

Prefer idempotent scripts where practical: rerunning with the same manifest should rebuild the same semantic asset even if binary files are not byte-identical.

## 5. Make revisions narrow

A revision starts from the previous manifest, not from a fresh interpretation of the original prose.

Example intent:

- V1 establishes generic body controls.
- V2 changes one requested control.
- locked controls remain identical in input and are checked in result metadata.

If an engine operation inherently perturbs other properties, expose that as a limitation instead of hiding it.

## 6. Use visual evidence strategically

Default character evidence during early phases:

- front
- three-quarter

Add side/back only when the claim being tested needs them. Later identity/canon work may justify a fixed four-view set or turntable.

Use consistent camera, focal length, framing, pose, lighting, and background across revision comparisons whenever possible. This makes visual drift easier to detect.

## 7. Stop when the slice is proven

Do not polish unrelated features after the success criterion is met. Synchronize docs and move to the next explicit slice.
