# Low-level and assembly layer

## Scope

naun-kernel is a small no_std crate. It deliberately contains only primitives that can be kept independent from a specific board:
- CPU spin-wait hint (cpu_relax);
- compiler and hardware ordering fences (full_memory_fence);
- volatile 8-bit and 32-bit MMIO reads/writes;
- compile-time architecture identification.

The main crate uses Rust inline assembly for x86/x86_64 (pause), ARM/AArch64 (yield), and RISC-V (nop). AVR currently takes the compiler's spin_loop fallback in the Rust crate; an optional AVR GNU assembler shim is included as a porting reference. The .S shims are not linked by the default Cargo build.

## Why not put everything in assembly?

Assembly belongs at the narrowest boundary that benefits from it: CPU hints, context-switch entry/exit, interrupt prologues, atomic primitives, startup code, and board-specific register access. Graph validation, data contracts, adapter policy, and orchestration benefit from Rust's type system and checked arithmetic. Keeping those layers separate prevents architecture-specific details from contaminating every integration.

## MMIO safety contract

The MMIO functions are unsafe because the caller must prove that the pointer:
1. is non-null and aligned for the access width;
2. maps a real device register;
3. uses a width permitted by that device;
4. remains valid for the duration of the access;
5. is accessed with the device's required ordering and synchronization rules.

A volatile access is not a cache-coherency protocol, DMA fence, lock, or interrupt controller. Board support packages must provide memory maps, pin muxing, clocks, reset sequencing, interrupt routing, DMA ownership, and peripheral-specific register definitions.

## Architecture support plan

| Target family | Current source | Additional platform work |
|---|---|---|
| x86 / x86_64 | Inline pause, GNU shim for x86_64 | APIC, PCI/PCIe, ACPI, boot protocol, cache and DMA rules |
| ARM / AArch64 | Inline yield, AArch64 GNU shim | GIC, MMU page tables, PSCI, device tree, DMA |
| RISC-V 32/64 | Inline nop, RISC-V64 GNU shim | SBI, PLIC/CLINT or AIA, page tables, device tree |
| AVR | Rust fallback, AVR GNU shim | AVR toolchain target, interrupt ABI, address-space and register model |

A source file or assembly shim is not proof that a board or target has been tested. CI should add cross-compilation jobs only when the matching Rust target and linker/toolchain are installed and the build is repeatable.

## Next kernel milestones

- board support package (BSP) trait and target-specific crates;
- linker scripts, reset/startup code, vector tables and panic handlers;
- typed register blocks generated from SVD or equivalent hardware descriptions;
- pin, clock, GPIO, UART, SPI, I2C, timer and watchdog abstractions;
- interrupt-safe queues and DMA ownership types;
- hardware-in-the-loop tests with documented board revisions.
