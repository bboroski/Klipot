/* Optional GNU assembler shim; the Rust kernel crate uses inline asm by default. */
.text
.global naun_arch_relax
.type naun_arch_relax,%function
naun_arch_relax:
    yield
    ret
.size naun_arch_relax, .-naun_arch_relax
