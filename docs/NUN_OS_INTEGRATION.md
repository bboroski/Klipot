# NUN OS integration contract — Klipot

## Ownership
Klipot owns developer-facing IDE, editor, project navigation and language-server integration. It consumes SAMBU target metadata and NUN diagnostic formats; it is not part of the boot chain or kernel runtime.

## Integration direction
1. Add NUN project templates for the supported kernel target and the host-side test target.
2. Consume versioned SAMBU target metadata and SaintSI ABI declarations rather than embedding compiler flags or syscall numbers.
3. Surface serial logs, panic summaries, QEMU exit status and symbolized backtraces as structured diagnostics.
4. Provide a launch profile that invokes the repository's documented build and QEMU scripts without changing kernel security settings.
5. Keep editor and LSP functionality optional so headless CI builds do not depend on Klipot.

## Acceptance gates
- A sample kernel project can be opened and its files, symbols and diagnostics indexed.
- Build and launch commands are reproducible and report nonzero failures.
- Debug symbols are matched to the exact kernel image hash.
- No IDE service is required for a successful kernel build or boot.

## Current status
Klipot is an optional developer tool. Remote GDB, source-level kernel debugging and NUN-specific LSP features remain future work until the kernel debug ABI is published.
