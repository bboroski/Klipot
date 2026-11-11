"""Platform target detection and profile checks for Klipot."""

from __future__ import annotations

import platform
import struct
import sys
from typing import Any, Mapping


E2K_ELF_MACHINE = 175
E2K_ISA_FAMILIES = (
    "e2k-v2", "e2k-v3", "e2k-v4", "e2k-v5", "e2k-v6", "e2k-v7"
)
E2K_QEMU_USER_ISA = ("elbrus-v2", "elbrus-v3", "elbrus-v4", "elbrus-v5", "elbrus-v6")


def normalize_architecture(machine: str) -> str:
    value = machine.strip().lower().replace("_", "-")
    if value in {"e2k", "elbrus", "mcst-elbrus"}:
        return "e2k"
    if value in {"amd64", "x86-64"}:
        return "x86_64"
    if value in {"arm64", "aarch64"}:
        return "aarch64"
    if value in {"i386", "i486", "i586", "i686", "x86"}:
        return "x86"
    return value or "unknown"


def detect_platform(
    *,
    machine: str | None = None,
    pointer_bits: int | None = None,
    byteorder: str | None = None,
    system: str | None = None,
) -> dict[str, Any]:
    raw = machine if machine is not None else platform.machine()
    arch = normalize_architecture(raw)
    bits = pointer_bits if pointer_bits is not None else struct.calcsize("P") * 8
    endian = byteorder if byteorder is not None else sys.byteorder
    os_name = (system if system is not None else platform.system()).lower()
    if bits not in (32, 64):
        raise ValueError("pointer_bits must be 32 or 64")
    if endian not in ("little", "big"):
        raise ValueError("byteorder must be little or big")
    is_e2k = arch == "e2k"
    return {
        "architecture": arch,
        "machine": raw,
        "operating_system": os_name,
        "word_bits": bits,
        "endianness": endian,
        "elf_machine": E2K_ELF_MACHINE if is_e2k else None,
        "native_e2k_linux": bool(is_e2k and os_name == "linux" and bits == 64 and endian == "little"),
    }


def validate_e2k_profile(profile: Mapping[str, Any]) -> tuple[str, ...]:
    """Return deterministic contract violations for an E2K target descriptor."""
    issues: list[str] = []
    if not isinstance(profile, Mapping):
        return ("profile must be an object",)
    if profile.get("architecture") != "e2k":
        issues.append("architecture must be e2k")
    elf = profile.get("elf")
    if not isinstance(elf, Mapping):
        issues.append("elf must be an object")
    else:
        if elf.get("class_bits") != 64:
            issues.append("E2K ELF class must be 64-bit")
        if elf.get("endianness") != "little":
            issues.append("E2K ELF must be little-endian")
        if elf.get("e_machine") != E2K_ELF_MACHINE:
            issues.append("ELF machine must be EM_MCST_ELBRUS (175)")
    linux = profile.get("linux")
    if not isinstance(linux, Mapping) or linux.get("uname_machine") != "e2k":
        issues.append("Linux machine name must be e2k")
    compiler = profile.get("compiler")
    if not isinstance(compiler, Mapping) or compiler.get("family") != "LCC":
        issues.append("compiler family must be MCST LCC")
    boot = profile.get("boot")
    if not isinstance(boot, Mapping) or boot.get("generic_limine") is not False:
        issues.append("E2K profile must not claim generic Limine boot support")
    emulation = profile.get("emulation")
    if not isinstance(emulation, Mapping) or "user-mode" not in str(emulation.get("qemu_e2k", "")):
        issues.append("qemu-e2k must be described as user-mode emulation")
    return tuple(issues)
