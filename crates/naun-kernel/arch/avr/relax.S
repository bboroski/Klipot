/* Optional avr-gcc shim; AVR is not compiled by the default workspace target. */
.text
.global naun_arch_relax
.type naun_arch_relax, @function
naun_arch_relax:
    nop
    ret
