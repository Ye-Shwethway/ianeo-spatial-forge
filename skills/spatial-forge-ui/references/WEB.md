# Spatial Forge Web / Mini App UI Rules

Apply to the current static viewer and later Telegram Mini App embedding.

## Primary Context

- Android phone first.
- Touch input first.
- The 3D model is the content; surrounding UI supports inspection.
- Static HTML/CSS/JS is preferred until product needs justify a framework.

## Layout

- Respect device safe areas for fixed headers/bottom controls.
- Use a single-column phone layout by default.
- Keep the 3D viewport prominent, typically occupying most of the first screen.
- Metadata can flow below the viewer or appear in a lightweight sheet/panel; do not permanently shrink the viewport with a desktop sidebar on phones.
- Avoid horizontal page scrolling.
- If fixed controls are used, add content inset so they do not cover scrollable content.

## Touch

- Primary touch targets should be roughly 48 CSS px or larger when practical.
- Keep at least about 8 px between neighboring touch targets.
- Use visible pressed/active feedback.
- Never rely on hover for required behavior.
- Do not require tiny icon-only targets for core actions.
- `Reset view`, preview selection, metadata opening, and downloads need obvious controls.

## Viewer States

Support explicit states:

- no model URL
- model loading
- model ready
- model load failure
- metadata loading
- metadata unavailable
- preview unavailable
- unsupported requested fields present

Keep error copy short and actionable. A broken model should not leave a blank unexplained canvas.

## Responsive Behavior

Minimum practical review widths:

- ~360 px small phone
- ~390–430 px common modern phone
- ~768 px tablet / large web view

The goal is not a giant viewport test matrix. Verify no horizontal overflow, readable controls, usable 3D area, and sensible metadata flow at representative sizes.

On larger screens, content may use a centered max-width shell or split viewport + metadata layout if it improves inspection. Do not force the phone layout to simply stretch edge to edge.

## Performance

- Avoid heavy frontend frameworks for the initial viewer.
- Keep layout stable while assets load.
- Give preview media explicit dimensions/aspect ratio.
- Load only what the current build needs.
- Lazy-load secondary images when useful.
- Do not add decorative animation that competes with WebGL/3D performance.
- Respect `prefers-reduced-motion` for nonessential motion.

## URL / Deep-Link Rule

Every inspectable build should be reachable from a shareable/deep-linkable URL. Preserve URL-driven model/metadata/preview inputs so Telegram can later open the same viewer without a second viewer implementation.

## Accessibility

- Semantic buttons for actions, not clickable generic containers.
- Visible keyboard focus remains required even though phone is primary.
- Labels must describe icon actions.
- Color cannot be the only status signal.
- Text contrast must remain readable over dark/neutral surfaces.
- Gesture interactions need visible alternatives for critical actions where practical.

## Avoid

- hamburger/drawer navigation for a one-screen inspector
- nested cards around every metadata row
- multiple competing accent colors
- permanent overlays covering important parts of the model
- automatic camera movement that fights the user's touch interaction
- tooltips as the only explanation of important controls on touch devices
