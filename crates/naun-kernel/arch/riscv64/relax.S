/* Optional GNU assembler shim; the Rust kernel crate uses inline asm by default. */
.text
.globl naun_arch_relax
.type naun_arch_relax,@function
naun_arch_relax:
    nop
    ret
.size naun_arch_relax, .-naun_arch_relax
