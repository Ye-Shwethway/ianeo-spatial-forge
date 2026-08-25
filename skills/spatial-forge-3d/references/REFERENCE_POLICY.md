# Blender / MPFB Reference Policy

Use this reference when implementation depends on exact Blender or MPFB behavior.

## Evidence hierarchy

For version-sensitive facts, prefer in this order:

1. behavior already runtime-proven in this repository on the pinned stack
2. official Blender documentation / Python API for the relevant version
3. official MPFB documentation/source/release information
4. direct source inspection of the installed extension/package
5. reputable agent-skill or community workflow as a methodology hint only

Community skills may improve process but must not override proven local runtime facts.

## Exact facts that require verification

Verify rather than guess:

- `bpy` operator/property names
- enum values
- Blender command-line flags
- extension installation behavior
- renderer availability
- GLTF exporter options
- MPFB macro/control names and valid ranges
- rig identifiers
- version compatibility
- defaults that affect output

## Runtime compatibility rule

The current proven project baseline is Blender `4.5.12 LTS` and MPFB `2.0.17`.

Do not copy commands or APIs from Blender 5.x-oriented skills without checking compatibility. A newer external reference is not evidence that the project should upgrade.

If an upgrade becomes necessary:

1. justify the concrete capability or bug requiring it
2. isolate the upgrade in its own slice
3. rerun the affected runtime proofs
4. inspect output artifacts again
5. update the documented baseline only after PASS

## Source-code truth

When documentation is ambiguous, inspect the installed package/source or run a minimal introspection probe rather than inventing behavior.

A tiny targeted runtime probe is preferable to a large speculative compatibility layer.

## External skill usage

Useful patterns observed in the broader Blender-agent ecosystem include:

- umbrella skill routing into focused specialists
- deterministic Python as durable source
- contract-first creation
- fixed multiview evidence
- authored-scene plus fresh-export validation
- visual feedback loops
- knowledge routing to exact Blender API references

Adopt these as design patterns, not dependencies. Keep Spatial Forge's own skill small and aligned with its runtime, privacy boundary, phone-first output, and slice-based development process.

## No silent precision

If the Creator requests a real-world measurement but MPFB exposes only a normalized macro control, preserve the original requested intent in metadata if useful, map only to the actual supported control, and label the mapping as approximate/control-based.

Never rename a normalized control to an exact physical unit just to make the interface appear more precise.
