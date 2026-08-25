# Spatial Forge Flutter UI Rules

Apply when a dedicated Flutter client becomes justified later.

## Principle

Do not redesign Spatial Forge merely because the implementation stack changes. Flutter should preserve the same product model, terminology, semantic tokens, information hierarchy, and inspection workflow as the web viewer unless a native capability creates a clear reason to differ.

## Structure

- Prefer simple feature-oriented folders and ordinary Flutter widgets over a large architecture framework.
- Reuse a small theme/token layer instead of hardcoding colors and spacing per screen.
- Add state management only when the screen state actually needs it.
- Keep navigation shallow and predictable.

## Adaptive Layout

- Respect `SafeArea` for fixed top/bottom controls.
- Phone first; adapt gutters and layout for tablet/landscape.
- Bottom navigation is only for genuine top-level destinations and should stay small in count.
- Do not mix multiple primary navigation patterns at the same hierarchy level.
- Preserve back-stack state and user inspection context.

## Touch and Feedback

- Android touch targets should be about 48x48 dp minimum for primary controls.
- Use Material press/ripple/state feedback where appropriate.
- Keep gaps between adjacent actions large enough to avoid accidental taps.
- Use haptics sparingly for meaningful confirmation, not every tap.
- Never redefine system back gestures or make critical operations gesture-only.

## 3D Inspection

If Flutter eventually embeds or implements the 3D viewer:

- preserve rotate/zoom/reset semantics from the web viewer
- prioritize smooth model interaction over decorative UI animation
- keep model loading and failure states explicit
- do not cover the model with persistent oversized panels
- preserve build metadata, preview comparison, and unsupported-field truthfulness

## Theme

Map the shared conceptual tokens into `ColorScheme`/ThemeExtension or an equally small theme mechanism. Keep light/dark choices semantically equivalent instead of manually recoloring every screen.

Typography should use a small number of roles, e.g. title, body, label, metadata/mono where needed. Support text scaling without clipped controls or broken layouts.

## Performance

- Avoid unnecessary widget rebuilds only where profiling or visible behavior shows a problem.
- Do not introduce broad performance abstractions preemptively.
- Use const widgets when natural, not as a ritual that harms readability.
- Keep heavy 3D/render work isolated from ordinary UI updates.
- Load previews/assets at sizes appropriate for the screen.

## Accessibility

- Provide semantic labels for icon-only actions.
- Maintain logical focus/traversal order.
- Do not use color as the only status indicator.
- Ensure text remains readable in both themes.
- Support reduced motion where custom motion exists.
- Test representative text scaling rather than assuming fixed font size.

## Native Features Worth Adding Only When Useful

Potential reasons to justify Flutter later include:

- offline/local asset cache
- richer gallery/history browsing
- side-by-side revision inspection
- native file sharing/download management
- deeper Simiverse integration

Do not build a dedicated client merely to duplicate a web viewer that already works well.
