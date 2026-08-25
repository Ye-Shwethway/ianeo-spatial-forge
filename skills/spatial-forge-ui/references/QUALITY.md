# Spatial Forge UI Quality Floor

Use this before calling a user-facing UI slice complete.

This is a focused product-quality checklist, not a broad visual-regression test matrix.

## 1. Purpose and Hierarchy

- The primary user task is obvious within a few seconds.
- The 3D model/preview is visually dominant on inspection screens.
- Primary action is distinguishable from secondary actions.
- Destructive or risky actions are separated from ordinary navigation/actions.
- Copy names operations in terms the Creator recognizes.

## 2. Touch and Interaction

- Important controls have comfortable touch areas (about 48 px/dp on Android-oriented surfaces where practical).
- Neighboring touch controls are not cramped.
- Pressed/selected/disabled states are visually clear.
- Core actions do not depend on hover.
- Critical gestures have visible alternatives where practical.
- System back/edge gestures are not hijacked.

## 3. Responsive / Safe Area

- No unintended horizontal page overflow on representative small and common phone widths.
- Fixed headers/bottom controls respect safe areas.
- Scroll content is not hidden behind fixed controls.
- Large screens adapt rather than merely stretching phone content.
- Model viewport remains meaningfully usable in portrait phone layout.

## 4. Accessibility

- Interactive elements use appropriate semantic elements/labels.
- Icon-only actions have descriptive accessible labels.
- Visible focus exists for keyboard-accessible web controls.
- Status is not conveyed by color alone.
- Primary text maintains strong readable contrast; aim for WCAG AA where applicable.
- Text scaling does not obviously clip or destroy critical controls.
- Nonessential motion respects reduced-motion preferences.

## 5. State Coverage

For any async/data-driven surface, explicitly consider the states that can really occur:

- loading
- success/ready
- empty/no asset
- unavailable/missing optional data
- failure
- disabled action
- unsupported requested precision

Do not invent elaborate states for impossible scenarios, but do not leave real failure modes as blank UI.

## 6. Performance and Stability

- Avoid layout jumps caused by unsized preview media.
- Avoid loading large nonessential assets before the primary viewer is usable.
- Do not add visual effects that materially degrade 3D interaction.
- Keep dependencies proportional to the surface.
- A lightweight viewer should remain lightweight.

## 7. Visual Consistency

- Shared semantic tokens are used instead of arbitrary per-screen colors.
- Spacing follows the project rhythm rather than random increments.
- Typography uses a small consistent role set.
- Radius, borders, elevation and icon style are coherent.
- One status meaning uses one semantic treatment across screens.

## 8. Real-Output Review

Before completion, inspect the rendered UI rather than reviewing source only.

Minimum practical review for the current web viewer:

- one small phone width around 360 px
- one common modern phone width around 390–430 px
- one larger/tablet width around 768 px when layout changes there
- model loading/ready behavior
- at least one failure or missing-input state if the current slice touches it

For Flutter later, use equivalent representative device sizes/orientations rather than a large device matrix unless a concrete regression requires one.

## Severity

Treat findings roughly as:

- **Blocker:** primary task cannot be completed, model cannot be inspected, major content inaccessible, serious privacy/security exposure
- **High:** unusable touch target, major overflow, unreadable contrast, broken state handling, system gesture conflict
- **Medium:** hierarchy/spacing inconsistency, weak feedback, awkward tablet behavior
- **Low:** cosmetic polish with no meaningful usability impact

Fix Blocker and High findings before calling the slice complete. Fix Medium when cheap and relevant. Do not delay a useful slice for low-value cosmetic perfection.
