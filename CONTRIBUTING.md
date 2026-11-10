# Contributing to NAUN

## Development checks

Before opening a pull request, run:

~~~bash
cargo fmt --all
cargo test --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
~~~

Keep dependencies minimal and explain every new runtime dependency. New system connectors should implement SystemAdapter and should not leak vendor SDK types into naun-core.

## Architecture rules

- Keep unsafe code inside the smallest hardware-specific boundary.
- Every unsafe function needs a precise Safety contract.
- Never treat in-process Arm implementations as sandboxed plugins.
- Validate graph input before performing side effects.
- Add protocol compatibility tests for any wire-format change.
- Hardware support claims must name the exact board revision, toolchain, and test evidence.

## Pull requests

Describe the problem, design, compatibility impact, tests run, and any limitations. Do not mark hardware support complete based only on compilation of an assembly shim.
