# Spatial Forge UI Design Intelligence

Use this skill for any Spatial Forge web UI, mobile web viewer, Telegram Mini App surface, or future Flutter UI work.

This is a project-specific design and UX routing skill. It intentionally keeps the useful workflow ideas from modern UI/UX design-intelligence systems while avoiding a giant generic style database or framework-specific bloat.

## Core Goal

Create interfaces that are:

- phone-first and touch-friendly
- visually calm enough that 3D content remains the focus
- consistent across web and future Flutter implementations
- fast to understand without desktop-oriented assumptions
- truthful about build/runtime state and unsupported precision
- accessible and resilient without turning the project into a UI test framework

## Required Workflow

Before implementing or materially changing UI:

1. **Frame the surface**
   - What is the user's main job on this screen?
   - Is this inspection, navigation, revision, status, download, or configuration?
   - What device/input context matters most?
   - What information is critical vs secondary?

2. **Define a compact design contract**
   Decide before coding:
   - one visual tone
   - semantic color roles
   - typography roles
   - spacing rhythm
   - radius/elevation language
   - one signature visual element at most
   - primary and secondary actions

   Do not redesign the visual language independently on every screen.

3. **Choose the platform route**
   - Static/mobile web or Telegram Mini App: read `references/WEB.md`.
   - Flutter: read `references/FLUTTER.md`.
   - Any user-facing UI: read `references/QUALITY.md`.

4. **Build the smallest real interaction**
   Prefer a working end-to-end surface over a broad component library. Reuse established tokens and components. Avoid speculative abstractions.

5. **See the real output**
   A UI change is not complete because markup compiles. Inspect the actual rendered result at the target phone width, exercise important states, and fix visible overflow, hierarchy, interaction, or contrast problems.

6. **Review against the quality floor**
   Use the checklist in `references/QUALITY.md`. Fix meaningful high-impact problems before calling the slice complete.

## Spatial Forge Visual Direction

Spatial Forge is an inspection and creation tool, not a marketing site.

Default direction:

- dark or neutral canvas-friendly visual system
- 3D viewport and preview imagery receive the largest visual weight
- metadata and controls use restrained surfaces around the content
- cyan/blue or another single cool accent may indicate selection/action, but do not scatter unrelated accent colors
- use semantic status colors only for real state meaning: success, warning, error, unsupported
- avoid decorative gradients, glass effects, oversized hero typography, excessive card nesting, and generic AI-dashboard clutter unless a future product need clearly justifies them
- keep labels literal and operational: `Open 3D`, `Reset view`, `Build details`, `Unsupported`, `Download GLB`

## Cross-Platform Token Rule

Web and Flutter should share the same conceptual tokens even when implementation syntax differs:

- `surface.canvas`
- `surface.panel`
- `surface.raised`
- `text.primary`
- `text.secondary`
- `border.subtle`
- `accent.primary`
- `state.success`
- `state.warning`
- `state.error`
- `state.unsupported`

Use a 4/8 spacing rhythm. Typical section spacing should come from a small set such as 8, 12, 16, 24, 32 rather than arbitrary per-screen values.

## 3D Viewer Interaction Rules

- The model is the primary content. Do not cover it with persistent large panels.
- Touch drag rotates; pinch zooms where the viewer supports it.
- Critical gestures must also have visible alternatives when practical, especially camera reset.
- Do not hijack Android/iOS system back/swipe gestures.
- Preview image tabs and metadata should remain reachable without precision tapping.
- Loading, model-load failure, missing metadata, and unsupported fields must have explicit states.
- Do not imply a model matches an exact real-world measurement unless the generation pipeline proved that precision.

## Scope Discipline

Do not add just because a design system could support it:

- giant component libraries
- elaborate animation frameworks
- global state management for a small static viewer
- large screenshot matrices during early slices
- full desktop-first navigation before there is a desktop need
- hidden gesture-only core actions
- visual polish that materially harms load/render performance

## Evidence Priority

For UX decisions, prefer in this order:

1. actual Creator feedback on the running Spatial Forge UI
2. rendered behavior on the target phone
3. existing Spatial Forge tokens/components
4. platform conventions and accessibility guidance
5. external design-intelligence references

External UI skills are methodology references, not automatic dependencies or sources of truth for Spatial Forge aesthetics.
